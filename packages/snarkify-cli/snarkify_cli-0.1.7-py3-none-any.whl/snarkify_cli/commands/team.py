import requests
import typer
from rich import print

from snarkify_cli.lib.command import logged_in_command
from snarkify_cli.lib.configs import CliConfig
from snarkify_cli.lib.http_utils import get_teams
from snarkify_cli.lib.prompt_utils import PROMPT_SELECTION_TYPE, CONSOLE, prompt_for_selection

team_app = typer.Typer(no_args_is_help=True, help="Gets team information and manages the team context.")


@logged_in_command(team_app, "list")
def list_team() -> None:
    """
    Lists all available teams.

    Displays a list of all teams you have access to. The team of your context is highlighted.
    """
    try:
        teams = get_teams()
    except requests.HTTPError as ex:
        print(f"Unable to retrieve teams due to {ex}")
        typer.Exit(code=1)
    else:
        for team_info in teams:
            if CliConfig.team_id == team_info["team_id"]:
                CONSOLE.print(f"> {team_info['name']}", style="bold yellow")
            else:
                CONSOLE.print(f"  {team_info['name']}")


@logged_in_command(team_app)
def switch() -> None:
    """
    Switches your active team.

    Allows you to switch to another team from the list of available teams.
    After selecting a team, it sets the chosen team as your active team.
    """
    try:
        teams = get_teams()
    except requests.HTTPError as ex:
        print(f"Unable to retrieve teams due to {ex}")
        typer.Exit(code=1)
    else:
        selected_team_idx = prompt_for_selection([t["name"] for t in teams], PROMPT_SELECTION_TYPE.TEAM)
        selected_team = teams[selected_team_idx]
        CliConfig.team_id = selected_team["team_id"]
        CliConfig.save()
        print(f"You've successfully switched to team {selected_team['name']}.")
