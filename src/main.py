"""
Main module for running the application.

This module sets up the logging configuration and loads the application configuration.
"""

import logging.config

# Setup logging once, as a global configuration
from config.logging_config import setup_logging
from config.config_loader import load_config

# Setup logging once, as a global configuration
setup_logging()

# Create a logger instance at the module level
logger = logging.getLogger('main')

# Load the configuration from the YAML files
config = load_config()

if __name__ == "__main__":
    # 提取配置值
    web_cookie = config['auth']['web_cookie']
    referer = config['auth']['referer']

    logger.info("Web Cookie: %s", web_cookie)
    logger.info("Referer: %s", referer)

    # Log some messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
