"""
Module for loading configuration from YAML files.
"""

import os

import yaml
from dotenv import load_dotenv

from src.config.config_path import CONFIG_DIR, PROJECT_ROOT_DIR


def load_config():
    """
    Loads configuration from YAML files.

    :return: Parsed configuration dictionary
    """
    # Construct configuration file paths
    main_config_path = os.path.join(CONFIG_DIR, 'config.yaml')
    secrets_config_path = os.path.join(CONFIG_DIR, 'secrets.yaml')

    # Read the main configuration file
    with open(main_config_path, 'r', encoding='utf-8') as file:
        wb_config = yaml.safe_load(file)

    # Read the secrets configuration file
    with open(secrets_config_path, 'r', encoding='utf-8') as file:
        secrets = yaml.safe_load(file)

    # Load .env
    load_dotenv(dotenv_path=PROJECT_ROOT_DIR / ".env")
    web_cookie = os.getenv('WEB_COOKIE')
    referer = os.getenv('REFERER')
    secrets['auth']['web_cookie'] = web_cookie
    secrets['auth']['referer'] = referer

    # Merge configuration information
    # config['auth'] = secrets['auth']
    wb_config.update(secrets)

    return wb_config
