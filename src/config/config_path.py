"""
Module for determining the configuration directory path.
"""

from pathlib import Path

# Get the path of the current file
current_file = Path(__file__).resolve()

PROJECT_ROOT_DIR = current_file.parent.parent.parent

# Define the configuration directory
CONFIG_DIR = PROJECT_ROOT_DIR / 'config'

# Uncomment for debugging
# print(f"Configuration directory: {CONFIG_DIR}")
