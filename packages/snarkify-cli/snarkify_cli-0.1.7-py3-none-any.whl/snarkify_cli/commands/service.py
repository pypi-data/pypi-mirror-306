import requests
import typer
from rich import print
from rich.table import Table

from snarkify_cli.lib.command import logged_in_command
from snarkify_cli.lib.configs import CliConfig, ProjectConfig
from snarkify_cli.lib.http_utils import create_service, get_service, list_services
from snarkify_cli.lib.prompt_utils import PROMPT_SELECTION_TYPE, CONSOLE, prompt_for_selection
from snarkify_cli.lib.service_utils import select_service_sku_price

service_app = typer.Typer(no_args_is_help=True, help="Manages service registration with Snarkify platform.")
DISPLAY_INFO_KEYS = [
    "service_id",
    "service_name",
    "team_name",
    "state",
    "created",
    "service_url",
    "image_tag",
]


@logged_in_command(service_app)
def create(name: str = typer.Argument(..., help="Service name")) -> None:
    """
    Registers a new service with Snarkify platform.

    Created service information will be cached in the working directory upon acknowledgement
    from Snarkify server. Subsequent attempts to re-create a service with existing cached
    service information will result in failure.
    """
    if ProjectConfig.service_id is not None:
        print("A service has already been initialized in the current directory.")
        raise typer.Exit(code=1)
    if CliConfig.team_id is None:
        print("Please select a team using `snarkify team switch`.")
        raise typer.Exit(code=1)
    try:
        team_id = CliConfig.team_id
        sku_id, price_id = select_service_sku_price(team_id)
        ProjectConfig.service_id = create_service(name, team_id, sku_id, price_id)
        ProjectConfig.save()
        print(f"Service {name} created successfully.")
    except Exception as ex:
        print(f"Service creation failure due to {ex}.")


@logged_in_command(service_app)
def info() -> None:
    """
    Retrieves service information.
    """
    if ProjectConfig.service_id is None:
        print("Service not initialized.")
        raise typer.Exit(code=1)
    service_info = get_service(ProjectConfig.service_id)
    table = Table(show_header=False, show_lines=True)

    for key in DISPLAY_INFO_KEYS:
        table.add_row(key.replace("_", " "), service_info[key])

    CONSOLE.print(table)


@logged_in_command(service_app, "list")
def list_registered_services() -> None:
    """
    Lists all available services.

    Displays a list of all services under current active team. The service of your context is highlighted.
    """
    if CliConfig.team_id is None:
        print("Please select a team using `snarkify team switch`.")
        raise typer.Exit(code=1)
    try:
        services = list_services(CliConfig.team_id)
    except requests.HTTPError as ex:
        print(f"Unable to retrieve services due to {ex}")
        raise typer.Exit(code=1)
    else:
        for service_info in services:
            if ProjectConfig.service_id == service_info["service_id"]:
                CONSOLE.print(f"> {service_info['service_name']}", style="bold yellow")
            else:
                CONSOLE.print(f"  {service_info['service_name']}")


@logged_in_command(service_app)
def switch() -> None:
    """
    Switches your active service.

    Allows you to switch to another service from the list of available services.
    After selecting a service, it sets the chosen service as your active service.
    """
    if CliConfig.team_id is None:
        print("Please select a team using `snarkify team switch`.")
        raise typer.Exit(code=1)
    try:
        services = list_services(CliConfig.team_id)
    except requests.HTTPError as ex:
        print(f"Unable to retrieve services due to {ex}")
        raise typer.Exit(code=1)
    else:
        selected_service_idx = prompt_for_selection(
            [t["service_name"] for t in services], PROMPT_SELECTION_TYPE.SERVICE
        )
        selected_service = services[selected_service_idx]
        ProjectConfig.service_id = selected_service["service_id"]
        ProjectConfig.save()
        print(f"You've successfully switched to service {selected_service['service_name']}.")
