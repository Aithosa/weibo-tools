"""
Module for setting up logging configuration from YAML files.
"""

import logging.config
import os
import yaml

from src.config.config_path import CONFIG_DIR


def create_log_dir(config_path):
    """
    Ensure the log directory exists.

    Args:
        config_path: Path to the logging configuration YAML file
    """
    with open(config_path, 'rt', encoding='utf-8') as config_file:
        wb_config = yaml.safe_load(config_file.read())
    log_file_path = wb_config['handlers']['file']['filename']
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created log directory: {log_dir}")


def setup_logging(
        default_path='',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """
    Setup logging configuration from a YAML file.

    Args:
        default_path: Default path to the logging configuration file
        default_level: Default logging level
        env_key: Environment variable key for logging configuration
    """
    config_path = os.path.join(CONFIG_DIR, 'logging.yaml') if not default_path else default_path
    value = os.getenv(env_key, None)

    if value:
        config_path = value

    if os.path.exists(config_path):
        create_log_dir(config_path)  # Ensure log directory exists before configuring logging
        with open(config_path, 'rt', encoding='utf-8') as config_file:
            wb_config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(wb_config)
    else:
        logging.basicConfig(level=default_level)
        logging.info("Logging configuration not found, using basicConfig.")
