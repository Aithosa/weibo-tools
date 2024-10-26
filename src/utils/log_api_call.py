"""
Module for logging API calls.

This module provides a decorator `log_api_call` to automatically log detailed information about API calls,
including their parameters and return values.

NOTE: This class is unused.
"""

import functools
import json
import logging

from src.config.logging_config import setup_logging

setup_logging()


def log_api_call(func):
    """
    Decorator that automatically logs the API call information.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the function name as the API name
        api_name = func.__name__

        default_logger = logging.getLogger('log_api_call_default')
        logger = getattr(args[0], 'logger', default_logger) if args else default_logger
        # logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")

        # Print the API name and parameters being called
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        # NOTE: this is not good, it prints function arguments
        logger.info("Calling API: %s(%s)", api_name, signature)

        # Call the original function
        result = func(*args, **kwargs)

        # Try to format the output value, use json.dumps for non-basic types to simplify output
        try:
            logger.info("Returned: %s", json.dumps(result, indent=None, ensure_ascii=False))
        except TypeError:  # if result is not JSON serializable
            logger.info("Returned: %s", result)

        return result

    return wrapper


if __name__ == "__main__":
    # Example function using the decorator
    @log_api_call
    def get_user_profile(user_id):
        """
        Assume this is an API call to get user profile.
        """
        # Simulated API call logic here
        profile = {
            "user_id": user_id,
            "username": "example_user",
            "email": "user@example.com"
        }
        return profile


    # Call the example function
    get_user_profile(123)
