"""Catch Exception decorator for CLI commands."""

import logging
import sys
from functools import wraps
from typing import Callable

from boto3.exceptions import Boto3Error
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)


class CLIError(Exception):
    """Default CLI Exception."""


def catch_exceptions(func: Callable) -> Callable:
    """
    Catches and simplifies expected errors thrown by CLI catch_exceptions should be used as a decorator.

    Args:
        func (`Callable`): The function which may throw exceptions which should be
        simplified.

    Returns:
        `Callable` The decorated function.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        """Invoke `func`, catches expected errors, prints the error message and exits with a non-zero exit code."""
        try:
            result = func(*args, **kwargs)
            return result
        except (CLIError, BotoCoreError, ClientError, Boto3Error) as error:
            logger.error(str(error))
            sys.exit(1)

    return decorated
