import os
import socket

import click

from file_processing import file_handling
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"success": "green", "error": "bold red", "fun": "purple"})


console = Console(theme=custom_theme)


def path_exists(path: str)-> bool:
    if os.path.exists(path):
        return True
    return False

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=10)
        return True
    except OSError:
        return False



@click.group()
def cli():
    pass

@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def write_doc(directory):
    source_code = file_handling.process_directory(directory)

    file_handling.create_markdown_file("./documentation", source_code)



cli.add_command(write_doc)


if __name__ == "__main__":
    cli()
