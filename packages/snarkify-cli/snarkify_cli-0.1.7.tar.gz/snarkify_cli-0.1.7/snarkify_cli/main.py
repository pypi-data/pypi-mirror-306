import typer
from rich.console import Console

from snarkify_cli.commands import auth, deployment, init, version
from snarkify_cli.commands.deployment import deployment_app
from snarkify_cli.commands.shell import shell_app
from snarkify_cli.commands.data import data_app
from snarkify_cli.commands.service import service_app
from snarkify_cli.commands.task import task_app
from snarkify_cli.commands.team import team_app

console = Console()
app = typer.Typer(help="Snarkify Command Line Interface", no_args_is_help=True)
auth.register_commands(app)
init.register_commands(app)
deployment.register_commands(app)
version.register_commands(app)
app.add_typer(team_app, name="team")
app.add_typer(service_app, name="service")
app.add_typer(task_app, name="task")
app.add_typer(data_app, name="data")
app.add_typer(shell_app, name="shell")
app.add_typer(deployment_app, name="deployment")


if __name__ == "__main__":
    app()
