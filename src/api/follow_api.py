"""
This module defines the FollowApi class for interacting with the Weibo follow API.

Classes:
    FollowApi: A class to interact with the Weibo follow API.
"""

import logging
from urllib.parse import urlencode

from requests import HTTPError

from src.api.base_api import BaseApi, remove_query_params


class FollowApi(BaseApi):
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

        super().__init__(session, config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_follow(self, page=1):
        """
        Retrieves the follow data from the Weibo follow API.
        example: "https://weibo.com/ajax/profile/followContent?page={}&next_cursor=50"

        Args:
            page (int, optional): The page number for paginated results. Defaults to 1.

        Returns:
            requests.Response: The response object from the request.
        """
        """
        Retrieves a paginated list of follow data from Weibo.

        Args:
            page (int, optional): The page number for pagination. Defaults to 1.

        Returns:
            dict: JSON response containing follow data for the specified page.
        """
        params = {
            'page': page,
        }
        query_string = urlencode(params, doseq=True, safe=':' """, encode_plus=False""")

        get_weibo_follow = self.config['urls']['follow']['get_weibo_follow']
        base_url = remove_query_params(get_weibo_follow)
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            response.raise_for_status()
            self.logger.info(
                f"Fetching follow list for UID {self.uid}, page {page}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def get_group(self, show_bilateral=1):
        """
        Fetches information about follow groups.
        example: "https://weibo.com/ajax/profile/getGroups?showBilateral=1"

        Args:
            show_bilateral (int, optional): Flag to include bilateral relationships. Defaults to 1.

        Returns:
            dict: JSON response with group details.
        """
        params = {
            'showBilateral': show_bilateral,
        }
        query_string = urlencode(params, doseq=True, safe=':' """, encode_plus=False""")

        get_profile_group = self.config['urls']['group']['get_profile_group']
        base_url = remove_query_params(get_profile_group)
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            response.raise_for_status()
            self.logger.info(f"Fetching follow group for UID {self.uid}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def create_group(self, name=None):
        """
        Creates a new follow group.
        example: "https://weibo.com/ajax/profile/createGroup" {"name":"test1"}

        Args:
            name (str): The name of the new group.

        Returns:
            dict: JSON response confirming group creation.
        """
        params = {
            'name': name,
        }
        params = {k: v for k, v in params.items() if v is not None}

        post_create_group = self.config['urls']['group']['post_create_group']
        base_url = remove_query_params(post_create_group)

        try:
            response = self.session.post(base_url, json=params)
            response.raise_for_status()
            self.logger.info(f"Creating follow group for UID {self.uid}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def update_group(self, name=None, is_open=True, list_id=None):
        """
        Updates properties of an existing follow group.
        example: "https://weibo.com/ajax/profile/updateGroup" {"name": "test1", "isOpen": true, "list_id": "5074698225844231"}

        Args:
            name (str, optional): New name for the group.
            is_open (bool, optional): Whether the group is open. Defaults to True.
            list_id (str, optional): Identifier of the group to update.

        Returns:
            dict: JSON response confirming group update.
        """
        params = {
            'name': name,
            'isOpen': is_open,
            'list_id': list_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        post_update_group = self.config['urls']['group']['post_update_group']
        base_url = remove_query_params(post_update_group)

        try:
            response = self.session.post(base_url, json=params)
            response.raise_for_status()
            self.logger.info(f"Updating follow group for UID {self.uid}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def destroy_group(self, list_id=None):
        """
        Deletes a follow group.
        example: "https://weibo.com/ajax/profile/destroyGroup" {"list_id": "5074698225844231"}

        Args:
            list_id (str): Identifier of the group to delete.

        Returns:
            dict: JSON response confirming group deletion.
        """
        params = {
            'list_id': list_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        post_destroy_group = self.config['urls']['group']['post_destroy_group']
        base_url = remove_query_params(post_destroy_group)

        try:
            response = self.session.post(base_url, json=params)
            response.raise_for_status()
            self.logger.info(f"Destroying follow group for UID {self.uid}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def get_user_group(self, uid=None):
        """
        Retrieves a specific user's follow groups.
        example: "https://weibo.com/ajax/profile/getGroupList?uid=5480863590"

        Args:
            uid (str, optional): User ID for whom to fetch groups. If not provided, may default to the authenticated user.

        Returns:
            dict: JSON response with the user's group list.
        """
        params = {
            'uid': uid,
        }
        query_string = urlencode(params, doseq=True, safe=':' """, encode_plus=False""")

        get_user_group = self.config['urls']['group']['get_user_group']
        base_url = remove_query_params(get_user_group)
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            response.raise_for_status()
            self.logger.info(f"Fetching follow group for UID {self.uid}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise

    def get_all_groups(self, is_new_segment=1, fetch_hot=1):
        """
        Fetches all available follow groups, optionally filtered by segment and popularity.
        example: "https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1"

        Args:
            is_new_segment (int, optional): Flag for fetching new segments. Defaults to 1.
            fetch_hot (int, optional): Flag for including hot groups. Defaults to 1.

        Returns:
            dict: JSON response with all follow groups.
        """
        params = {
            'is_new_segment': is_new_segment,
            'fetch_hot': fetch_hot,
        }
        query_string = urlencode(params, doseq=True, safe=':' """, encode_plus=False""")

        get_all_groups = self.config['urls']['group']['get_all_groups']
        base_url = remove_query_params(get_all_groups)
        formatted_url = f"{base_url}?{query_string}"

        try:
            response = self.session.get(formatted_url)
            response.raise_for_status()
            self.logger.info(f"Fetching all follow groups for UID {self.uid}. Response status: {response.status_code}")

            parsed_response = self._check_and_return_json(response)
            return parsed_response
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise
