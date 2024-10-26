"""
This module defines the BlogApi class, which provides methods for interacting with Weibo's blogging features.
It includes functionalities to fetch blog lists, original blog posts, and long-text content,
as well as download images associated with blog posts.

Classes:
    BlogApi: A class for interacting with Weibo's blog API.
"""

import logging
import time
from urllib.parse import urlencode, urlparse, unquote

from requests.exceptions import HTTPError, ChunkedEncodingError, RequestException

from src.api.base_api import BaseApi, remove_query_params

logging.basicConfig(level=logging.INFO)


class BlogApi(BaseApi):
    """
    BlogApi is a specialized API client for interacting with Weibo's blogging features.
    It inherits from BaseApi and adds methods to fetch blog lists, original blog posts, and long-text content.

    Attributes:
        session: The session object to make HTTP requests.
        config: The configuration dictionary containing necessary settings.
        logger: The logger to log information.
    """

    def __init__(self, session=None, config=None, uid=None):
        """
        Initialize the BlogApi instance with a session, configuration, and optionally a user ID.

        Args:
            session (requests.Session, optional): An HTTP session for making requests. Defaults to None.
            config (dict, optional): Configuration dictionary for API endpoints and settings. Defaults to None.
            uid (str, optional): The user ID for whose blog posts to fetch. Defaults to None.
        """
        super().__init__(session, config)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.uid = uid

    def get_blog_list(self, uid=None, page=1, feature=0, since_id=None):
        """
        Retrieve a list of blog posts for a given user ID, supporting pagination and filtering options.
        example: "https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0&since_id=5051758198395820"

        Args:
            uid (str, optional): The user ID. Can also be set during class initialization.
            page (int, optional): The page number to fetch. Defaults to 1.
            feature (int, optional): A feature filter, typically for sorting. Defaults to 0.
            since_id (str, optional): The ID of the last seen post for fetching newer posts. Defaults to None.

        Returns:
            dict: JSON response from the API containing the blog post list.

        Raises:
            ValueError: If the user ID (`uid`) is not provided.
            HTTPError: If the request encounters an HTTP error.
        """
        # Ensure uid is provided either via class initialization or method argument
        uid = uid or self.uid
        if uid is None:
            raise ValueError("User ID (uid) must be provided either in constructor or as a method argument.")

        # Prepare URL parameters, automatically excluding None values
        params = {
            'uid': uid,
            'page': page,
            'feature': feature,
            'since_id': since_id,
        }
        # Use urlencode to construct the query string, it will ignore keys with None values
        query_string = urlencode(params, doseq=True, safe=':')

        # query_string = urlencode(params, doseq=True)
        base_url = remove_query_params(self.config['urls']['blog']['get_weibo_list_url'])
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            self.logger.info("Fetching blog list for UID %s, page %s. Response status: %s",
                             uid, page, response.status_code)
            return response.json()
        except HTTPError as http_err:
            self.logger.error("HTTP error occurred: %s", http_err)
            raise

    def get_original_blog_list(self, uid=None, page=1, since_id=None, hasori=None):
        """
        Fetch a list of original blog posts for a user, with options for pagination and filtering original content.
        example: "https://weibo.com/ajax/statuses/searchProfile?uid={}&page={}&since_id=5057294913504845&hasori={}"

        Args:
            uid (str, optional): The user ID. Can also be initialized with the class.
            page (int, optional): Page number for pagination. Defaults to 1.
            since_id (str, optional): Since ID for newer posts. Defaults to None.
            hasori (bool, optional): Flag to filter original posts. Defaults to None.

        Returns:
            dict: JSON response from the API containing the original blog post list.

        Raises:
            ValueError: If no user ID is provided.
            HTTPError: On unsuccessful HTTP request.
        """
        uid = uid or self.uid
        if uid is None:
            raise ValueError("User ID (uid) must be provided either in constructor or as a method argument.")

        params = {
            'uid': uid,
            'page': page,
            'since_id': since_id,
            'hasori': hasori,
        }

        query_string = urlencode(params, doseq=True)
        base_url = remove_query_params(self.config['urls']['blog']['get_search_profile_url'])
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            response.raise_for_status()
            self.logger.info("Fetching original blog list for UID %s, page %s. Response status: %s",
                             uid, page, response.status_code)
            return response.json()
        except HTTPError as http_err:
            self.logger.error("HTTP error occurred: %s", http_err)
            raise

    def get_weibo_longtext(self, mblogid=None):
        """
        Retrieve the full text of a long-form blog post given its ID.
        example: "https://weibo.com/ajax/statuses/longtext?id={}"

        Args:
            mblogid (str, required): The unique identifier of the blog post.

        Returns:
            dict: JSON response from the API containing the long text of the blog post.

        Raises:
            ValueError: If the post ID is not provided.
            HTTPError: On unsuccessful HTTP request.
        """
        if mblogid is None:
            raise ValueError("mblogid must be provided either in constructor or as a method argument.")

        params = {'id': mblogid}
        query_string = urlencode(params, doseq=True)
        base_url = remove_query_params(self.config['urls']['blog']['get_weibo_longtext_url'])
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            response.raise_for_status()
            self.logger.info("Fetched blog longtext for ID %s. Response status: %s",
                             mblogid, response.status_code)
            return response.json()
        except HTTPError as http_err:
            self.logger.error("HTTP error occurred: %s", http_err)
            raise

    def download_image(self, image_url, mblogid=None):
        """
        Download an image from a specified URL.

        Args:
            image_url (str, required): The URL of the image to be downloaded.
            mblogid (str, optional): The microblog ID for logging purposes.

        Returns:
            tuple: A tuple containing the filename and raw content of the HTTP response.

        Raises:
            ValueError: If image_url is not provided.
            HTTPError: If an HTTP error occurs during the image download.
        """
        if image_url is None:
            raise ValueError("image_url must be provided either in constructor or as a method argument.")

        max_retries = 3
        for _ in range(max_retries):
            try:
                response = self.session.get(image_url, stream=True, timeout=30)
                # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                response.raise_for_status()

                parsed_url = urlparse(image_url)
                path = parsed_url.path
                filename = unquote(path.split('/')[-1])
                self.logger.info("Downloading blog image for ID %s from %s", mblogid, image_url)
                return filename, response.raw
            except (ChunkedEncodingError, HTTPError, RequestException) as error:
                self.logger.error("An error occurred while downloading the image: %s", error)
                time.sleep(2)

        self.logger.error("Failed to download the image after %d attempts", max_retries)
        return None, None
