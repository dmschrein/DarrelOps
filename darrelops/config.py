"""This module provides the config functionality."""
# darrelops/config.py

from pathlib import Path
import typer
from darrelops import (
    __app_name__
)

CONFIG_DIR = Path(typer.get_app_dir("__app_name__"))
CONFIG_