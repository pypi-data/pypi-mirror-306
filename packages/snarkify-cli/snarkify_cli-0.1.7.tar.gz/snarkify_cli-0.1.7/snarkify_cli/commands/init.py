import typer
from rich import print

from snarkify_cli.lib.command import logged_in_command
from snarkify_cli.lib.init_utils import add_rust_dependency, create_rust_project_template


def register_commands(app: typer.Typer):
    @logged_in_command(app)
    def init(lang: str = typer.Option(..., "--lang", help="Language option", case_sensitive=False)) -> None:
        """
        Initialize a new project with the specified language in current directory.

        Currently only Rust is supported.
        """
        if lang.lower() not in ["rust"]:
            print("Invalid language. Please choose 'rust'.")
            raise typer.Exit(1)
        # Rust initialization logic
        print("Initializing project...")
        create_rust_project_template()
        add_rust_dependency()
