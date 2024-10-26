"""
This module provides the BaseApi class and utility functions to handle user ID extraction and URL manipulation,
as well as setting up HTTP sessions for API interactions.
"""

import logging
from urllib.parse import urlparse, urlunparse

from requests import Response

from src.config.config_loader import load_config
from src.utils.logging_session import LoggingSession


def extract_user_id(referer):
    """
    Extracts the user ID from the referer URL.

    Args:
        referer (str): The referer URL.

    Returns:
        str: User ID extracted from the URL path.
    """
    parsed_url = urlparse(referer)
    path_parts = parsed_url.path.strip('/').split('/')
    user_id = path_parts[-1] if path_parts else None
    return user_id


def get_uid(config):
    """
    Retrieves the user ID from the configuration.

    Args:
        config (dict): Configuration settings containing the 'auth' key.

    Returns:
        str: User ID from the configuration.

    Raises:
        ValueError: If the user ID could not be determined from the configuration.
    """
    referer = config['auth']['referer']
    uid = extract_user_id(referer)
    if uid is None:
        raise ValueError("User ID (uid) must be provided either in constructor or as a method argument.")
    return uid


def remove_query_params(url):
    """
    Removes query parameters from the URL and returns the base URL without parameters.

    Args:
        url (str): Original URL that may contain query parameters.

    Returns:
        str: URL without query parameters.
    """
    parsed_url = urlparse(url)
    no_query_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, '', parsed_url.fragment))
    return no_query_url


class BaseApi:
    """
    Base API class providing common functionalities for API interactions.

    Attributes:
        session: The session object to make HTTP requests.
        config: The configuration dictionary containing necessary settings.
        logger: The logger to log information.
    """

    def __init__(self, session=None, config=None):
        """
        Initializes the BaseApi with a session and config.

        Args:
            session (requests.Session, optional): HTTP session for requests. Defaults to None.
            config (dict, optional): Configuration settings. Defaults to None.
        """
        if config is None:
            self.config = load_config()
        else:
            self.config = config

        if session is None:
            self.session = self.create_session_from_config()
        else:
            self.session = session
        self.uid = get_uid(self.config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_session_from_config(self, config=None):
        """
        Creates a session object with headers configured from the config.

        Args:
            config (dict, optional): Configuration settings. Defaults to None.

        Returns:
            requests.Session: Configured session object.
        """
        if config is None:
            config = self.config

        web_cookie = config['auth']['web_cookie']
        referer = config['auth']['referer']
        session = LoggingSession()
        header = {
            'Referer': referer,
            'Cookie': web_cookie,
            'User-Agent': "Mozilla/5.0 ...",
            'Authorization': "Bearer ..."
        }
        session.headers.update(header)
        return session

    def _check_and_return_json(self, response: Response):
        """
        Checks if the response can be JSON parsed and returns the parsed content.
        Logs and raises an exception if the response cannot be parsed.

        Args:
            response (requests.Response): The HTTP response to check and parse.

        Returns:
            dict: Parsed JSON content from the response.

        Raises:
            ValueError: If the response content is not a valid JSON.
        """
        try:
            return response.json()
        except ValueError as value_err:
            self.logger.info("Response content is not a valid JSON: %s", response.text)
            self.logger.error("Failed to parse response as JSON: %s", value_err)
            raise ValueError("Response content is not a valid JSON.") from value_err
