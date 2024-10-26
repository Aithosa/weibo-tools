"""
This module defines the ApiManager class which is used to manage API interactions.

NOTE: This class is unused.
"""

import logging

from src.api.base_api import BaseApi
from src.api.blog_api import BlogApi
from src.api.favorites_api import FavoriteApi
from src.api.follow_api import FollowApi


class ApiManager(BaseApi):
    """
    Manages API interactions by providing APIs for follow, blog, and favorite operations.
    """

    def __init__(self, session=None, config=None):
        """
        Initializes the ApiManager with a session and config.
        
        Args:
            session (requests.Session, optional): HTTP session for requests. Defaults to None.
            config (dict, optional): Configuration settings. Defaults to None.
        """
        super().__init__(session, config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_follow_api(self):
        """
        Returns an instance of FollowApi.
        
        Returns:
            FollowApi: Instance of FollowApi.
        """
        return FollowApi(session=self.session, config=self.config)

    def get_blog_api(self):
        """
        Returns an instance of BlogApi.
        
        Returns:
            BlogApi: Instance of BlogApi.
        """
        return BlogApi(session=self.session, config=self.config)

    def get_favorite_api(self):
        """
        Returns an instance of FavoriteApi.
        
        Returns:
            FavoriteApi: Instance of FavoriteApi.
        """
        return FavoriteApi(session=self.session, config=self.config)


if __name__ == "__main__":
    # Using ApiManager to Instantiate API Classes
    api_manager = ApiManager()
    follow_api = api_manager.get_follow_api()
    blog_api = api_manager.get_blog_api()
    favorite_api = api_manager.get_favorite_api()
