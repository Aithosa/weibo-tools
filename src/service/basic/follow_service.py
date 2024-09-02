"""
Module to handle follow service operations, including fetching, merging,
and compressing follow data.
"""

import json
import logging
import os
import re
import shutil
import subprocess
from datetime import datetime
from src.api.follow_api import FollowApi
from src.config.config_loader import load_config


def get_project_root():
    """Return the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


class FollowService:
    """Service to handle follow operations."""

    def __init__(self):
        """Initialize FollowService with configurations and API."""
        self.config = load_config()
        self.follow_api = FollowApi(config=self.config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_data_path(self):
        """Return the configured data path."""
        project_root = get_project_root()
        config_data_path = self.config['base']['data_path']
        return os.path.join(project_root, config_data_path)

    def get_all_follow(self):
        """Fetch all follow data and save it into files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_dir = os.path.join(self.get_data_path(), 'raw', 'follow', timestamp)
        os.makedirs(save_dir, exist_ok=True)

        count = []
        page = 1

        while True:
            response = self.follow_api.get_follow(page)
            if response.status_code != 200:
                self.logger.error(
                    "Error: Received status code %d, Response Content: %s",
                    response.status_code, response.text
                )
                break

            try:
                json_content = response.json()
            except ValueError:
                self.logger.error(
                    "Error: Response content is not valid JSON. Response Content: %s",
                    response.text
                )
                break

            try:
                follows = json_content['data']['follows']
                next_cursor = follows.get('next_cursor')
                previous_cursor = follows.get('previous_cursor')
                total_number = follows.get('total_number')

                users = follows.get('users', [])
                count.append(len(users))
                if not all(isinstance(x, int) for x in [next_cursor, previous_cursor, total_number]):
                    raise ValueError("Invalid cursor or total_number values")

                self.logger.info(
                    "Processing page %d: previous_cursor %d, next_cursor %d, total_number %d, HTTP Status Code: %d",
                    page, previous_cursor, next_cursor, total_number, response.status_code
                )
                with open(os.path.join(save_dir, f'response{page}.json'), 'w', encoding='utf-8') as file:
                    json.dump(json_content, file, ensure_ascii=False, indent=4)
                self.logger.info("Response %d saved to %s/response%d.json", page, save_dir, page)

                if next_cursor == 0:
                    break

            except ValueError:
                with open(os.path.join(save_dir, f'response{page}.txt'), 'w', encoding='utf-8') as file:
                    file.write(response.text)
                self.logger.info("Response %d saved to %s/response%d.txt", page, save_dir, page)

            page += 1

        self.logger.info("-----check follow counts----- %s", count)
        output_file = self.merge_follow_files(save_dir)

        # Should return output_file?
        return output_file

    def merge_follow_files(self, source_folder):
        """Merge all follow JSON files in the provided folder into a single JSON file with a timestamped name."""
        all_users = []
        files = sorted([f for f in os.listdir(source_folder) if f.endswith('.json')],
                       key=lambda x: int(x.replace('response', '').replace('.json', '')))

        if not files:
            self.logger.info("No JSON files found in %s directory.", source_folder)
            return None

        first_file_path = os.path.join(source_folder, files[0])
        with open(first_file_path, 'r', encoding='utf-8') as file:
            first_json_content = json.load(file)

        count = []

        for file_name in files:
            file_path = os.path.join(source_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                json_content = json.load(file)
                users = json_content['data']['follows'].get('users', [])
                count.append(len(users))
                all_users.extend(users)

        first_json_content['data']['follows']['users'] = all_users
        self.logger.info("-----check follow counts----- %s", count)

        timestamp = self.get_timestamp(source_folder)
        save_dir = os.path.join(self.get_data_path(), 'processed', 'follow')
        os.makedirs(save_dir, exist_ok=True)
        output_file = os.path.join(save_dir, f'merged_follows_{timestamp}.json')
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(first_json_content, file, ensure_ascii=False, indent=4)
        self.logger.info("All JSON files have been merged into %s.", output_file)
        return first_json_content

    def get_timestamp(self, source_folder):
        """Extract timestamp from the folder name, or generate a new one."""
        timestamp_pattern = r'\d{8}_\d{6}'
        match = re.search(timestamp_pattern, source_folder)
        if match:
            timestamp = match.group(0)
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return timestamp

    def compress_and_commit(self, output_file):
        """Compress a single file and commit it to a Git repository."""
        base_name = os.path.basename(output_file)
        name_without_extension = os.path.splitext(base_name)[0]
        zip_dir = os.path.dirname(output_file)
        # zip_file = os.path.join(zip_dir, f"{name_without_extension}.zip")

        # 确定当前工作目录
        current_dir = os.getcwd()

        # 创建一个路径来存储压缩文件的位置
        zip_file_path = os.path.join(current_dir, zip_dir, f"{name_without_extension}.zip")

        # 压缩文件位置
        archive_name = os.path.join(zip_dir, name_without_extension)

        # 确保压缩文件的目录存在
        if not os.path.exists(zip_dir):
            os.makedirs(zip_dir)

        # 创建压缩文件
        shutil.make_archive(archive_name, 'zip', zip_dir, base_name)
        self.logger.info("File '%s' has been compressed into '%s'.", output_file, zip_file_path)

        try:
            # 添加压缩文件到Git仓库并提交修改
            subprocess.check_call(['git', 'add', zip_file_path])
            commit_message = f"Add compressed follow file {zip_file_path}"
            subprocess.check_call(['git', 'commit', '-m', commit_message])
            subprocess.check_call(['git', 'push'])
            self.logger.info("'%s' has been committed and pushed to the remote repository.", zip_file_path)
        except subprocess.CalledProcessError as e:
            self.logger.error("An error occurred while executing git command: %s", e)
