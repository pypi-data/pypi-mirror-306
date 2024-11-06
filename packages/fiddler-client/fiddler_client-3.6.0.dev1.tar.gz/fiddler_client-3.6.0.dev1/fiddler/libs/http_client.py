from __future__ import annotations

import time
from copy import deepcopy
from typing import Any
from urllib.parse import urljoin

import requests
import simplejson
from requests.adapters import HTTPAdapter

import fiddler.libs.aws
from fiddler.constants.common import JSON_CONTENT_TYPE
from fiddler.exceptions import HttpError, BaseError  # pylint: disable=redefined-builtin
from fiddler.libs.json_encoder import RequestClientJSONEncoder
from fiddler.utils.logger import get_logger

log = get_logger(__name__)

# Note(JP): this is doing conditional runtime modification for AWS Hadron /
# SageMaker, depending on
# - environment variables set by the user
# - importability of the AWS sagemaker Python SDK
# TODO: type annotation w/o having to import PartnerAppAuthProvider? This thing
# is either None or an instantiated auth provider.
_AWS_SM_AUTH_PROVIDER = fiddler.libs.aws.conditionally_init_aws_sm_auth()  # type: ignore


class RequestClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        verify: bool = True,
        proxies: dict | None = None,
    ) -> None:
        """
        HTTP client abstraction.

        For centralized logging and retrying and error handling
        """

        # The default retry mechanism keep retrying HTTP requests up to a
        # certain deadline N seconds in the future. The idea is to survive
        # micro outages, i.e. this should be O(1 min). Idea: make configurable,
        # maybe have a conservative default and then we can tune this in our CI
        # to try longer.
        self.default_retry_for_seconds = 60 * 10
        self.timeout_long_running_requests = (5, 120)
        self.timeout_short_running_requests = (5, 15)

        self.base_url = base_url
        self.proxies = proxies
        self.headers = headers
        self.headers.update({'Content-Type': JSON_CONTENT_TYPE})
        self.session = requests.Session()

        # Note(JP): from the AWS SageMaker partner app guide.
        if _AWS_SM_AUTH_PROVIDER is not None:
            # Get callback class (`RequestsAuth` type`) from SM auth provider,
            # and decorate the `requests` session object with that. This is
            # enabling the magic of automatically mutating request headers.
            # Among others, this injects the SigV4 header.
            self.session.auth = _AWS_SM_AUTH_PROVIDER.get_auth()

        self.session.verify = verify
        adapter = HTTPAdapter(
            # Note(JP): what's the relevance of setting these?
            pool_connections=25,
            pool_maxsize=25,
        )

        # Does mounting the custom HTTP adapter revert the session.auth
        # change from above?
        self.session.mount(self.base_url, adapter)

    def _request_with_retry(
        self,
        *,
        method: str,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        data: dict | bytes | None = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Emit HTTP request.

        Always apply retry strategy, unless told not to.

        :param method: HTTP method like
        :param url: API endpoint
        :param params: Query parameters
        :param headers: Request headers
        :param data: Dict/binary data
        :param timeout: Request timeout in seconds
        :param kwargs: passed on to requests.session.request()
        """
        abs_url = urljoin(self.base_url, url)
        request_headers = self.headers

        # override/update headers coming from the calling method
        if headers:
            request_headers = deepcopy(self.headers)
            request_headers.update(headers)

        content_type = request_headers.get('Content-Type')
        if data is not None and content_type == JSON_CONTENT_TYPE:
            # Why did we decide on simplejson here instead of stdlib? For
            # behavior, for perf?
            data = simplejson.dumps(
                data, ignore_nan=True, cls=RequestClientJSONEncoder  # type: ignore
            )

        # Use `setdefault`: define properties in kwargs when the caller doesn't
        # specify. verify: default to session config, but allow for override.
        kwargs.setdefault('allow_redirects', True)
        kwargs.setdefault('verify', self.session.verify)

        # Construct dictionary of parameters passed to session.request() with
        # all parameters except for method and URL.
        kwargs.update(
            {
                "params": params,
                "data": data,
                "headers": request_headers,
                "timeout": timeout,
                "proxies": self.proxies,
            }
        )

        return self._make_request_retry_until_deadline(method, abs_url, **kwargs)

    def _make_request_retry_until_deadline(
        self, method: str, url: str, **kwargs: Any
    ) -> requests.Response:
        """
        Return `requests.Response` object when the request was sent out and
        responded to with an HTTP response with a 2xx status code.

        Implement a retry loop with deadline control.

        Raise an exception derived from `requests.exceptions.RequestException`
        to indicate a non-retryable error, such as various 4xx responses.

        Interrupt the retry loop and raise ryingHTTPClientNonRetryableResponse

        Raise `fiddler.exceptions.BaseError` (from last exception) when
        reaching the deadline (it might raise a minute early, or even be
        briefly exceeded).
        """
        logpfx = f"http: {method} {url} --"

        t0 = time.monotonic()
        deadline = t0 + self.default_retry_for_seconds
        cycle: int = 0

        log.debug("%s try", logpfx)

        while time.monotonic() < deadline:
            cycle += 1

            result = self._make_request_retry_guts(method, url, **kwargs)

            if isinstance(result, requests.Response):
                if cycle > 1:
                    log.info("%s success after %.3f s", logpfx, time.monotonic() - t0)
                return result

            # Rename, for clarity. This exception was considered retryable, but
            # we may have to throw it below upon approaching the deadline.
            last_exception = result

            # Desired behavior: rather fast first retry attempt; followed by
            # slow exponential growth, and an upper bound: 0.66, 1.33, 2.66,
            # 5.33, 10.66, 21.33, 42.66, 60, 60, .... (seconds)
            wait_seconds = min((2**cycle) / 3.0, 60)
            log.info(
                "%s cycle %s failed, wait for %.1f s, deadline in %.1f min",
                logpfx,
                cycle,
                wait_seconds,
                (deadline - time.monotonic()) / 60.0,
            )

            # Would the next wait exceed the deadline?
            if (time.monotonic() + wait_seconds) > deadline:
                break

            time.sleep(wait_seconds)

        # Give up after retrying. Structurally emit error detail of last seen
        # (retryable) exception.
        raise BaseError(
            f"{method} request to {url}: giving up after {time.monotonic() - t0:.3f} s"
        ) from last_exception

    def _make_request_retry_guts(
        self, method: str, url: str, **kwargs: Any
    ) -> requests.Response | requests.RequestException:
        """
        Return `requests.Response` object when the request was sent out and
        responded to with an HTTP response that does not throw upon
        `resp.raise_for_status()` (a 2xx status code).

        Return an exception object to indicate a _retryable_ error to the
        caller. The caller will then retry.

        Raise an exception derived from `requests.exceptions.RequestException`
        to indicate a non-retryable error, such as various 4xx responses.
        """
        logpfx = f"http: {method} {url} --"

        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout_long_running_requests

        # Magic argument passed down to here. Can be set to "off".
        retry_strategy = kwargs.pop('retry', 'default')

        t0 = time.monotonic()
        log.info("%s emit", logpfx)

        try:
            # Here, we want to have a tight TCP connect() timeout and a
            # meaningful TCP recv timeout, also a meaningful global
            # request-response cycle timeout (accounting for the ~expected HTTP
            # request processing time in the API implementation, plus leeway).
            resp = self.session.request(method=method, url=url, **kwargs)
        except requests.exceptions.RequestException as exc:

            if retry_strategy == "off":
                log.info("%s error: %s", logpfx, exc)
                # Do not retry, let the caller deal with this exception.
                raise

            # Note(JP): we did not get a response. We might not even have sent
            # the request. An error happened before sending the request, while
            # sending the request, while waiting for response, or while
            # receiving the response. High probability for this being a
            # transient problem. A few examples for errors handled here:
            #
            # - DNS resolution error
            # - TCP connect() timeout
            # - Connection refused during TCP connect()
            # - Timeout while waiting for the other end to start sending the
            #   HTTP response (after having sent the request).
            # - RECV timeout between trying to receive two response bytes.
            #
            # Note(JP): do this, regardless of the type of request that we
            # sent. I know we've expressed concerns about idempotency here and
            # there. But I believe that it will be a big step forward to have
            # more or less *easy-to-reason-about* retrying in the client and to
            # maybe risk a rare idempotency problem and debug it and fix it in
            # the backend.

            # Convention: returning the exception tells the caller to retry.
            log.info("%s retry soon: %s", logpfx, exc)
            return exc

        # Got an HTTP response. In the scope below, `resp` reflects that.
        log.info(
            "%s request took %.3f s, response code: %s, resp body size: %s, req body size: %s",
            logpfx,
            time.monotonic() - t0,
            resp.status_code,
            len(resp.content),
            0 if resp.request.body is None else len(resp.request.body),
        )

        try:
            resp.raise_for_status()

            # The criterion for a good-looking response. Ideally we check for
            # the _precisely_ expected status code, but can do that later.
            return resp
        except requests.HTTPError as exc:
            # Decide whether or not this is a retryable based on the response
            # details. Put into a log message before leaving this function.
            treat_retryable = self._is_retryable_resp(resp)

            # Log body prefix: sometimes this is critical for debuggability.
            log.warning(
                "%s error response with code %s%s, body bytes: <%s ...>",
                logpfx,
                resp.status_code,
                " (treat retryable)" if treat_retryable else "",
                resp.text[:500],
            )

            if retry_strategy == "off":
                raise

            if treat_retryable:
                return exc

            # Otherwise let this nice requests.HTTPError object bubble up to
            # calling code. This is the expected code path for most 4xx
            # error responses.
            raise

    def _is_retryable_resp(self, resp: requests.Response) -> bool:
        """
        Do we (want to) consider this response as retryable, based on the
        status code alone?
        """
        if resp.status_code == 429:
            # Canonical way to signal "back off, retry soon".
            return True

        if resp.status_code == 501:
            # Means: "not implemented" or "not supported". Might be a little
            # exotic to use but we seem to rely on it. Do not retry those
            # for now, in general
            return False

        # Retry any 5xx response, later maybe fine-tune this by specific status
        # code. Certain 500 Internal Server Error are probably permanent, but
        # it's worth retrying them, too.
        if str(resp.status_code).startswith("5"):
            return True

        return False

    def get(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: float | tuple[float, float] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def delete(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='DELETE',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | bytes | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='POST',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def put(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='PUT',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def patch(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self._request_with_retry(
            method='PATCH',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )
