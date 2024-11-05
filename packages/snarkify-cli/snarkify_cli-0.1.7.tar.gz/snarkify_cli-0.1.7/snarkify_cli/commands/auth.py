import requests
import typer
from InquirerPy import prompt
from rich import print

from snarkify_cli.lib.configs import CliConfig
from snarkify_cli.lib.command import command
from snarkify_cli.lib.http_utils import get_teams
from snarkify_cli.lib.prompt_utils import PROMPT_SELECTION_TYPE, prompt_for_selection


def register_commands(app: typer.Typer):
    @command(app)
    def login() -> None:
        """
        Logs in Snarkify.

        Prompts you to enter your API key and select a team to complete the login process.
        """
        if CliConfig.has_auth():
            print("You have already logged in, please log out first to re-login.")
            return
        answer_name = "api_key"
        questions = [{"type": "password", "message": "Enter your api-key:", "name": answer_name}]
        answers = prompt(questions)
        CliConfig.api_key = answers[answer_name]
        try:
            teams = get_teams()
        except requests.HTTPError as ex:
            print(f"Unable to verify the api-key due to {ex}")
        else:
            selected_team_idx = prompt_for_selection([t["name"] for t in teams], PROMPT_SELECTION_TYPE.TEAM)
            selected_team = teams[selected_team_idx]
            CliConfig.team_id = selected_team["team_id"]
            CliConfig.save()
            print("You have successfully logged in.")

    @command(app)
    def logout() -> None:
        """Logs out Snarkify."""
        if not CliConfig.has_auth():
            print("You haven't logged in yet.")
            return
        CliConfig.remove()
        print("You have successfully logged out.")
