"""
offlix - A tool to manage and deploy Docker services.

This package provides functionality to start, stop, and manage various services
using Docker Compose.
"""

__version__ = "0.1.0"
__author__ = "Suman Manna"
__email__ = "manna.suman134@gmail.com"
from offlix_installer.installer import start_service, get_service_env, read_env_file, save_env_to_file

# Define what’s available when using 'from <package> import *'
__all__ = [
    'start_service',
    'get_service_env',
    'read_env_file',
    'save_env_to_file'
]