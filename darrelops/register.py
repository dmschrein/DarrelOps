"""This module provides the Darrel Ops server functionality."""
# darrelops/register.py

from pathlib import Path
import configparser

import typer 

from darrelops import (
    REG_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, CONFIG_FILE, __app_name__
)

REGISTER_DIR_PATH = Path(typer.get_app_dir(__app_name__)) # update to call HTTP API
REGISTER_FILE_PATH = REGISTER_DIR_PATH / "config.ini" # update to store the program in a directory

# Register the C program

def register_program(name: str, repo_url: str, build_cmd: str, build_dir: Path) -> None:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config[name] = {
        "repo_url": repo_url,
        "build_cmd": build_cmd,
        "build_dir": str(build_dir),
    }
    with CONFIG_FILE.open("w") as configfile:
        config.write(configfile)
    print(f"C program '{name}' registered successfully.")``