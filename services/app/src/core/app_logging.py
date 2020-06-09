"""
Logging handlers, formatters, and other classes, methods, and variables for
TinyDevCRM logging.
"""

import functools
import logging
import sys


@functools.lru_cache
def get_broker_logger():
    """
    Returns a properly formatted logger for the broker custom 'django-admin'
    process.

    Returns:
        logging.Logger
    """
    logger = logging.getLogger('broker')
    logger.setLevel(logging.DEBUG)

    # Create formatter for log message types.
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create handler to stream logs to stdout.
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
