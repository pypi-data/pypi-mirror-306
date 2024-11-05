import typer
from rich import print
from snarkify_cli.context import __version__, ENV
from snarkify_cli.lib.command import command


def register_commands(app: typer.Typer):
    @command(app)
    def version() -> None:
        """Shows the current version and environment of Snarkify CLI."""
        print(f"Snarkify CLI Version: {__version__} ({ENV} environment)")
