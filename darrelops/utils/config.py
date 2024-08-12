"""This module provides the config functionality."""
# darrelops/config.py

from pathlib import Path
import typer
from .constants import PROGRAMS_JSON_PATH
import os
import json

def get_config_dir():
    from darrelops import __app_name__
    return Path(typer.get_app_dir("__app_name__"))

class DbConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///artifactory.db'


def load_programs():
    """Load registered programs from JSON file."""
    if os.path.exists(PROGRAMS_JSON_PATH):
        with open(PROGRAMS_JSON_PATH, 'r') as file:
            return json.load(file)
    return []