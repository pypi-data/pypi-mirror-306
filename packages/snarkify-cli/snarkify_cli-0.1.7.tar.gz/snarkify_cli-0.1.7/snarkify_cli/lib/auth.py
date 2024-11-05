from functools import wraps
from typing import Any, Dict

import typer

from snarkify_cli.lib.configs import CliConfig
from snarkify_cli.lib.exception import AuthError


def get_auth_header() -> Dict[str, Any]:
    if not CliConfig.has_auth():
        raise AuthError("api-key not configured yet, please login first!")
    return {"x-api-key": CliConfig.api_key}


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not CliConfig.has_auth():
            typer.echo("Please login to run this command!")
            raise typer.Exit(code=1)

        try:
            return func(*args, **kwargs)
        except AuthError as ex:
            typer.echo(ex.message)

    return wrapper
