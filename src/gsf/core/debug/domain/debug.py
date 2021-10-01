"""Debug Module
=====================
This module contains the definition of a functions and decorators to manage logging tools
used in the framework.

Example:
    Creating a debug log over a function or method::

        @debug("Debug log")
        def fun():
            pass
"""

import functools

from loguru import logger
import sys

config = {
    "handlers": [
        {
            "sink": sys.stderr,
            "level": "INFO",
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{"
                      "message}</level>",
        }
    ]
}
"""Logger configuration."""

logger.configure(**config)


def debug(message: str = "", after: bool = False):
    """Debug decorator."""

    def real_decorator(function):
        @functools.wraps(real_decorator)
        def wrapper(*args, **kwargs):
            if not after:
                logger.debug(
                    "["
                    + str(function.__module__).split(".")[-1]
                    + "] "
                    + function.__name__
                    + str(args[1:])
                    + " "
                    + message
                )
                return function(*args, **kwargs)
            logger.debug(
                "["
                + str(function.__module__).split(".")[-1]
                + "] "
                + function.__name__
                + str(args[1:])
                + " "
                + message
            )
            return function(*args, **kwargs)

        wrapper.__doc__ = function.__doc__
        return wrapper

    return real_decorator


def enable_debug():
    """Enables the debug logs."""
    logger.remove()
    new_config = {
        "handlers": [
            {
                "sink": sys.stderr,
                "level": "DEBUG",
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{"
                          "message}</level>",
            }
        ]
    }
    logger.remove()
    logger.configure(**new_config)
