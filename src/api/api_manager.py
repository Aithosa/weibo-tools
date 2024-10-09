import logging

import requests

from src.api.base_api import get_uid
from src.api.blog_api import BlogApi
from src.api.favorites_api import FavoriteApi
from src.api.follow_api import FollowApi
from src.config.config_loader import load_config
from src.utils.logging_session import LoggingSession


class ApiManager:
    def __init__(self, session=None, config=None):
        """
        Initializes the ApiManager with a session and config.

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

    def get_follow_api(self):
        return FollowApi(session=self.session, config=self.config)

    def get_blog_api(self):
        return BlogApi(session=self.session, config=self.config)

    def get_favorite_api(self):
        return FavoriteApi(session=self.session, config=self.config)


if __name__ == "__main__":
    # Using ApiManager to Instantiate API Classes
    api_manager = ApiManager()
    follow_api = api_manager.get_follow_api()
    blog_api = api_manager.get_blog_api()
    favorite_api = api_manager.get_favorite_api()
