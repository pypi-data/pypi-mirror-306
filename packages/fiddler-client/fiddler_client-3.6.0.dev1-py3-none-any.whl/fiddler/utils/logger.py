import logging
import sys
from logging import Logger

from fiddler.constants.common import LOG_FORMAT, LOGGER_NAME


def get_logger(name: str) -> Logger:
    """Get logger instance"""
    logger: Logger = logging.getLogger(name)

    # Note(JP): this assumes that get_logger() is only called once per name.
    # Typically, the null handler is added to stop propagation of log messages
    # to user's stderr in case they do _not_ configure a logging outlet (think:
    # the null handler stops propagation into the "last resort handler").
    # Future: the null handler only needs to be added _once_ to the fiddler-client
    # logger hierarchy (to the top-level logger).
    logger.addHandler(logging.NullHandler())
    return logger


def set_logging(level: int = logging.INFO) -> None:
    """Set app logger at given log level"""
    app_logger = logging.getLogger(LOGGER_NAME)
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    app_logger.addHandler(handler)
    app_logger.setLevel(level)
