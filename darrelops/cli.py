"""This module provides the Darrel Ops CLI."""
# darrelops/cli.py 

from typing import Optional
from pathlib import Path
import typer

from darrelops import ERRORS, __app_name__, __version__, database, artifactory, register

app = typer.Typer()

# add the register c program command
@app.command()
def register(
    reg_path: Path = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
    ),
    c_program_path: Path = typer.Option(  
        None,
        "--register",
        "-r",
        help="Path to the C program to register and build.",
    ),
) -> None:
    """Registers the C program"""
    reg_program_error = register.reg_program(reg_path) # initialize a database to store information about the C program
    if reg_program_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[reg_program_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    # register the C program
    reg_init_error = register.init_database(reg_path) # could change the init and config for register to the git solution
    if reg_init_error:
        typer.secho(
            f'Registering C program failed with "{ERRORS[reg_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {reg_path}", fg=typer.colors.GREEN)
    """Build the C program"""
    if c_program_path:
        if not c_program_path.exists():
            typer.secho(
                f"The C program path '{c_program_path}' does not exist.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    # call build function
    build_program_error = 
        
        
        
        
        
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return 