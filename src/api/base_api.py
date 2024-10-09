import logging
from urllib.parse import urlparse, urlunparse

import requests
from requests import Response

from src.config.config_loader import load_config
from src.utils.logging_session import LoggingSession


def extract_user_id(referer):
    parsed_url = urlparse(referer)
    path_parts = parsed_url.path.strip('/').split('/')
    user_id = path_parts[-1] if path_parts else None
    return user_id


def get_uid(config):
    referer = config['auth']['referer']
    uid = extract_user_id(referer)

    if uid is None:
        raise ValueError("User ID (uid) must be provided either in constructor or as a method argument.")
    return uid


def remove_query_params(url):
    """
    移除URL中的查询参数并返回无参数的基础URL。

    :param url: 原始URL，可能包含查询参数。
    :return: 无查询参数的URL。
    """
    parsed_url = urlparse(url)
    # 重新构建URL，忽略parse_qs得到的查询参数部分
    no_query_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, '', parsed_url.fragment))
    return no_query_url


class BaseApi:
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
        # session = requests.session()
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
        except ValueError as e:
            self.logger.info(f"Response content is not a valid JSON: {response.text}")
            self.logger.error(f"Failed to parse response as JSON: {e}")
            raise ValueError("Response content is not a valid JSON.") from e
