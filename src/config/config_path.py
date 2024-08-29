"""
Module for determining the configuration directory path.
"""

from pathlib import Path

# Get the path of the current file
current_file = Path(__file__).resolve()

# Define the configuration directory
CONFIG_DIR = current_file.parent.parent.parent / 'config'

# Uncomment for debugging
# print(f"Configuration directory: {CONFIG_DIR}")
