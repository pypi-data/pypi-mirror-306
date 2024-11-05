import functools
from typing import Optional

import typer

from snarkify_cli.lib.auth import login_required
from snarkify_cli.lib.exception import handle_uncaught_errors


def command(app: typer.Typer, name: Optional[str] = None):
    def decorator(func):
        @functools.wraps(func)
        @app.command(name=name)
        @handle_uncaught_errors
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return decorator


def logged_in_command(app: typer.Typer, name: Optional[str] = None):
    def decorator(func):
        @functools.wraps(func)
        @app.command(name=name)
        @handle_uncaught_errors
        @login_required
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return decorator
