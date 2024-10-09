import logging

from requests import HTTPError

from src.api.base_api import BaseApi, remove_query_params


class PostApi(BaseApi):
    """
    A class to interact with the Weibo post API.

    Attributes:
        session (requests.Session): The active session for making HTTP requests.
        config (dict): Configuration dictionary with URLs and other settings required for API interactions.
        logger (logging.Logger): Logger instance for tracking actions and responses.
    """

    def __init__(self, session=None, config=None):
        """
        Initializes the WeiboPostApi instance with a session and configuration settings.

        Args:
            session (requests.Session, optional): The session for managing requests. Defaults to None.
            config (dict, optional): Configuration details including API endpoints. Defaults to None.
        """
        super().__init__(session, config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def delete_weibo(self, post_id=None):
        """
        Deletes a weibo post based on the provided post ID.
        example: "https://weibo.com/aj/mblog/del?ajwvr=6"

        Args:
            post_id (int): The unique identifier of the post to be deleted.

        Returns:
            dict: JSON response from the server after deletion attempt.

        Raises:
            HTTPError: If an HTTP error occurs during the deletion request.
        """
        form_data = {
            'mid': str(post_id)
        }

        post_delete_url = self.config['urls']['post']['post_delete_url']
        base_url = remove_query_params(post_delete_url)

        try:
            response = self.session.post(base_url, data=form_data)
            response.raise_for_status()
            self.logger.info(f"Deleting blog for UID {self.uid}. Response status: {response.status_code}")

            return response.json()
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def post_weibo(self, content=None):
        """
        Posts a new weibo entry with the specified content.
        example: "https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=1510279745199"

        Args:
            content (str): The content to be posted on Weibo.

        Returns:
            dict: JSON response from the server after posting attempt.

        Raises:
            HTTPError: If an HTTP error occurs during the posting request.
        """
        form_data = {
            'location': 'v6_content_home',
            'text': content,
            'appkey': '',
            'style_type': '1',
            'pic_id': '',
            'tid': '',
            'pdetail': '',
            'rank': '0',
            'rankid': '',
            'module': 'stissue',
            'pub_source': 'main_',
            'pub_type': 'dialog',
            'isPri': '0',
            '_t': '0',
        }

        add_weibo_url = self.config['urls']['post']['add_weibo_url']
        base_url = remove_query_params(add_weibo_url)

        try:
            response = self.session.post(base_url, data=form_data)
            response.raise_for_status()
            self.logger.info(f"Posting blog for UID {self.uid}. Response status: {response.status_code}")

            return response.json()
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise
