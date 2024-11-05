import functools

import click
import typer
from rich import print


def handle_uncaught_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except click.exceptions.Exit as e:
            raise e
        except Exception as e:
            print(f"An error occurred: {e}")
            raise typer.Exit(1)

    return wrapper


class AuthError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
