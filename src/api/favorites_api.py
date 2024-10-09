import logging
from urllib.parse import urlencode

from requests import HTTPError

from src.api.base_api import BaseApi, remove_query_params


class FavoriteApi(BaseApi):
    def __init__(self, session=None, config=None, uid=None):
        """
        Initialize the FavoriteApi with an optional session and configuration.

        Args:
            session (requests.Session, optional): An existing HTTP session for making requests. Defaults to None.
            config (dict, optional): A dictionary containing configuration settings such as API URLs. Defaults to None.
            uid (str, optional): User ID required for favorite operations. Can be provided during initialization or per method call. Defaults to None.
        """
        super().__init__(session, config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_all_favorites(self, uid=None, page=1, with_total=True):
        """
        Fetches a list of all favorites for a specified user ID with pagination support.
        example: "https://weibo.com/ajax/favorites/all_fav?uid={}&page={}&with_total=true"

        Args:
            uid (str, optional): The user ID for which to fetch favorites. If not provided, uses the uid set during initialization.
            page (int, optional): The page number for paginated results. Defaults to 1.
            with_total (bool, optional): Whether to include the total count of favorites in the response. Defaults to True.

        Returns:
            dict: JSON response containing favorites data.

        Raises:
            ValueError: If no user ID (uid) is provided either during initialization or as a method argument.
            HTTPError: If the HTTP request fails with an unsuccessful status code.
        """
        # Ensure uid is provided either via class initialization or method argument
        uid = uid or self.uid
        if uid is None:
            raise ValueError("User ID (uid) must be provided either in constructor or as a method argument.")

        # Prepare URL parameters, automatically excluding None values
        params = {
            'uid': uid,
            'page': page,
            'with_total': with_total,
        }
        # Use urlencode to construct the query string, it will ignore keys with None values
        query_string = urlencode(params, doseq=True, safe=':' """, encode_plus=False""")

        # Construct the final URL
        get_all_favorites_url = self.config['urls']['favorites']['get_all_favorites_url']
        base_url = remove_query_params(get_all_favorites_url)
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            self.logger.info(
                f"Fetching favorites blog list for UID {uid}, page {page}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def get_favorites_tag(self, page=1, is_show_total=1):
        """
        Retrieves a list of tags associated with favorites, with pagination and total count option.
        example: "https://weibo.com/ajax/favorites/tags?page={}&is_show_total=1"

        Args:
            page (int, optional): The page number for paginated results. Defaults to 1.
            is_show_total (int, optional): Whether to display the total number of tags. Defaults to 1 (True).

        Returns:
            dict: JSON response containing favorites tags data.

        Raises:
            HTTPError: If the HTTP request fails with an unsuccessful status code.
        """
        # Prepare URL parameters, automatically excluding None values
        params = {
            'page': page,
            'is_show_total': is_show_total,
        }
        # Use urlencode to construct the query string, it will ignore keys with None values
        query_string = urlencode(params, doseq=True, safe=':' """, encode_plus=False""")

        # Construct the final URL
        get_favorites_tag_url = self.config['urls']['favorites']['get_favorites_tag_url']
        base_url = remove_query_params(get_favorites_tag_url)
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            self.logger.info(f"Fetching favorites tag, page {page}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    # 修改收藏的标签，查看收藏的标签
