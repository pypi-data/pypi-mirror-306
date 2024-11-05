import json

import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text

from snarkify_cli.lib.command import logged_in_command
from snarkify_cli.lib.configs import ProjectConfig
from snarkify_cli.lib.http_utils import create_task, get_task
from snarkify_cli.tasks.constants import DETAILED_TASK_FIELDS
from snarkify_cli.tasks.enums import TaskField
from snarkify_cli.lib.websocket_utils import loop_for_task_logs

task_app = typer.Typer(no_args_is_help=True, help="Manages tasks with Snarkify platform.")


@logged_in_command(task_app)
def create(
    json_str: str = typer.Option(None, "--json", help="JSON string"),
    file_path: str = typer.Option(None, "--file", help="File path"),
) -> None:
    """
    Create a new task.
    """
    if ProjectConfig.service_id is None:
        print("No service has been initialized in the current directory.")
        raise typer.Exit(code=1)

    if json_str is None and file_path is None:
        print("Please specify either --json or --file.")
        raise typer.Exit(code=1)

    # Task input needs to be a JSON string
    input_str = None
    if json_str is not None:
        input_str = json_str
    else:
        try:
            with open(file_path, "r") as f:
                input_str = f.read()
        except Exception as ex:
            print(f"Error reading file: {ex}")
            raise typer.Exit(code=1)
    try:
        # Convert the JSON string to a dictionary
        params = {"input": json.loads(input_str)}
        task_id = create_task(ProjectConfig.service_id, params)
        print(f"Task {task_id} created successfully. Check status with `snarkify task info {task_id}`")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        raise typer.Exit(1)
    except Exception as ex:
        print(f"Task creation failure due to {ex}.")
        raise typer.Exit(1)


@logged_in_command(task_app)
def info(
    task_id: str = typer.Argument(..., help="Task id"),
    show_details: bool = typer.Option(False, "--details", "-d", help="Show detailed results"),
) -> None:
    """
    Retrieves task information.
    """
    task_info = get_task(task_id)
    console = Console()
    table = Table(show_header=False, show_lines=True)

    for key in TaskField:
        if key in DETAILED_TASK_FIELDS and not show_details:
            continue
        table.add_row(
            key.value.replace("_", " "), Text(task_info[key.value] if task_info[key.value] else "", overflow="fold")
        )
    console.print(table)


@logged_in_command(task_app)
def log(
    task_id: str = typer.Argument(..., help="Task id"),
) -> None:
    """
    Retrieves task logs.
    """
    loop_for_task_logs(task_id)
