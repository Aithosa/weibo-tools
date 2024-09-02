"""
This module defines the FollowApi class for interacting with the Weibo follow API.

Classes:
    FollowApi: A class to interact with the Weibo follow API.
"""

import logging
import requests
from src.config.config_loader import load_config


class FollowApi:
    """
    A class to interact with the Weibo follow API.

    Attributes:
        session: The session object to make HTTP requests.
        config: The configuration dictionary containing necessary settings.
        logger: The logger to log information.
    """

    def __init__(self, session=None, config=None):
        """
        Initializes the FollowApi with a session and config.

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

        session = requests.session()
        header = {
            'Referer': referer,
            'Cookie': web_cookie,
            'User-Agent': "Mozilla/5.0 ...",
            'Authorization': "Bearer ..."
        }
        session.headers.update(header)

        return session

    def get_follow(self, page=1):
        """
        Retrieves the follow data from the Weibo follow API.

        Args:
            page (int, optional): The page number for paginated results. Defaults to 1.

        Returns:
            requests.Response: The response object from the request.
        """
        get_weibo_follow = self.config['urls']['get_weibo_follow']
        response = self.session.get(get_weibo_follow.format(page))
        return response
