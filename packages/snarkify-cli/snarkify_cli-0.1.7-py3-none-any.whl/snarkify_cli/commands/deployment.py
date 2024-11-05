import os
from typing import List, Optional
import requests

import typer
from docker.errors import ImageNotFound
from rich import print
from rich.table import Table

from snarkify_cli.lib.aws_utils import upload_file_to_s3
from snarkify_cli.lib.configs import ProjectConfig, CliConfig
from snarkify_cli.lib.docker_utils import func_build, save_image
from snarkify_cli.lib.command import logged_in_command
from snarkify_cli.lib.http_utils import (
    create_service_image,
    deploy_service,
    update_service_env_vars,
    get_deployment,
    list_deployments,
)
from snarkify_cli.lib.prompt_utils import CONSOLE


deployment_app = typer.Typer(no_args_is_help=True, help="Manages service deployment history with Snarkify platform.")


DISPLAY_DEPLOYMENT_INFO_KEYS = [
    "build_id",
    "service_id",
    "service_name",
    "state",
    "created",
    "started",
    "finished",
    "commit",
    "image_tag",
    "image_id",
    "data_id",
]


def register_commands(app: typer.Typer):
    @logged_in_command(app)
    def build(
        base_dir: str = typer.Option(
            default="",
            help="The directory where to run the build command, default to current directory",
        )
    ):
        """
        Builds the docker image locally.
        """
        if not ProjectConfig.service_id:
            print("Project not initialized yet.")
            raise typer.Exit(code=1)
        func_build(ProjectConfig.service_id, base_dir)

    @logged_in_command(app)
    def deploy(
        tag: str = typer.Option(default="", help="Image tag"),
        image_name: Optional[str] = typer.Option(
            None,
            "--image",
            help="Full image name in the form [REPOSITORY]:[TAG]",
        ),
        env_strs: List[str] = typer.Option(
            [],
            "--env",
            help="Environment variables in key=value format, set value to none or null (case insensitive) for deletion",
        ),
    ):
        """
        Deploys the built docker image to snarkify platform.

        example usages:\n
        1. Assign a unique tag to this deployment\n
        snarkify deploy --tag feature_abc\n
        2. Update environment variables along with this deployment\n
        snarkify deploy --env foo=bar --env hello=aloha
        3. Use your custom image name in this deployment\n
        snarkify deploy --image docker.io/snarkfy/my-image-name:latest
        """
        if not ProjectConfig.service_id:
            print("Project not initialized yet.")
            raise typer.Exit(code=1)
        if CliConfig.team_id is None:
            print("Please select a team using `snarkify team switch`.")
            raise typer.Exit(code=1)

        # parse environment variables
        env_vars = {}
        for env_str in env_strs:
            try:
                key, value = env_str.split("=", 1)
                env_vars[key] = None if value.lower() in ["none", "null"] else value
            except ValueError:
                print(f"Invalid environment variable: '{env_str}', please use the KEY=VALUE form")
                raise typer.Exit(code=1)

        service_id = ProjectConfig.service_id
        tar_file_name = f"{service_id}.tar"
        try:
            print(f"Creating temporary image tar file as {tar_file_name}")
            save_image(tar_file_name, image_name)
            image_info = create_service_image(service_id, tag)
            print("Starting image uploading, this may take a while...")
            upload_res = upload_file_to_s3(tar_file_name, image_info["uri"])
            if upload_res.status_code == 200:
                if env_vars:
                    print("Updating service environment variables")
                    update_service_env_vars(service_id, env_vars)
                print("Image uploaded successfully, starting server side deployment")
                deploy_service(service_id, image_info["image_id"])
                print(
                    "Deployment started, expect it to be done in a few minutes, "
                    "please check status with `snarkify service info`"
                )
            else:
                print(f"Failed to upload image due to {upload_res.text}")
        except ImageNotFound:
            print("Image not found, please run snarkify build first.")
        except Exception as ex:
            print(f"Deployment failed due to {repr(ex)}")
            raise ex
        finally:
            if os.path.exists(tar_file_name):
                os.remove(tar_file_name)


@logged_in_command(deployment_app)
def info(deployment_id: str = typer.Argument(..., help="Deployment ID")) -> None:
    """
    Retrieves deployment information.
    """
    deployment_info = get_deployment(deployment_id)
    table = Table(show_header=False, show_lines=True)

    for key in DISPLAY_DEPLOYMENT_INFO_KEYS:
        if key not in deployment_info:
            continue
        table.add_row(key.replace("_", " "), str(deployment_info.get(key, "")))

    CONSOLE.print(table)


@logged_in_command(deployment_app)
def list(
    service_id: Optional[str] = typer.Argument(None, help="Service ID"),
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    size: int = typer.Option(3, "--size", "-s", help="Page size"),
) -> None:
    """
    Lists deployments under a service.

    Displays a list of deployments under a service, including deployment ID, created time, and state.
    If service_id is not specified, it will use the default service id under current working directory.
    """
    if service_id is None:
        service_id = ProjectConfig.service_id
        if service_id is None:
            print("Please specify a service ID to check deployments.")
            raise typer.Exit(code=1)
    try:
        deployments = list_deployments(service_id, page, size)
    except requests.HTTPError as ex:
        print(f"Unable to retrieve deployments due to {ex}")
        raise typer.Exit(code=1)
    else:
        table = Table(show_header=False, show_lines=True)
        table.add_row("Deployment ID", "Created Time", "State")
        for deployment_info in deployments.get("items", []):
            deployment_id = deployment_info.get("build_id", "")
            state = deployment_info.get("state", "")
            created = deployment_info.get("created", "")
            table.add_row(deployment_id, created, state)
        CONSOLE.print(table)
        print(
            f"Total: {deployments.get('total', 0)}, page: {deployments.get('page', 0)}, size: {deployments.get('size', 0)}, pages: {deployments.get('pages', 0)}"
        )
