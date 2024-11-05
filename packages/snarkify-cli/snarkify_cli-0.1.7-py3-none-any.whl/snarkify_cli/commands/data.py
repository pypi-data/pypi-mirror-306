from pathlib import Path
from typing import List

import typer
from rich import print
from rich.table import Table

from snarkify_cli.lib.aws_utils import upload_file_to_s3
from snarkify_cli.lib.command import logged_in_command
from snarkify_cli.lib.configs import ProjectConfig
from snarkify_cli.lib.http_utils import (
    get_linked_service_data,
    create_service_data,
    get_service,
    get_service_data_upload_urls,
    list_service_data_items,
)
from snarkify_cli.lib.prompt_utils import CONSOLE

data_app = typer.Typer(no_args_is_help=True, help="Manages data that will be consumed by the service in context.")
DATA_ITEM_HEADER = ["File Name", "Last Modified", "Size (B)"]


@logged_in_command(data_app)
def upload(files_or_dirs: List[Path] = typer.Argument(..., help="a list of files separated by space")) -> None:
    """
    Upload the given list of files/directories to Snarkify platform and accessible to the current service.

    Please note:\n
        1. Uploaded files will be placed in the /snarkify_data directory\n
        2. Relative path of files under an uploaded directory will be preserved, but the paths to the file/directory will not. \n
        For example, if you upload a file /home/user/foo and a directory /home/user/bar(which has two files inside: x and param/y),\n
        you will have the following mapping:\n
        /home/user/foo -> /snarkify_data/foo\n
        /home/user/bar/x -> /snarkify_data/bar/x\n
        /home/user/bar/param/y -> /snarkify_data/bar/param/y\n
    """
    if ProjectConfig.service_id is None:
        print("Project not initialized yet.")
        raise typer.Exit(code=1)

    linked_data_id = get_linked_service_data(ProjectConfig.service_id)
    if linked_data_id is None:
        service_info = get_service(ProjectConfig.service_id)
        linked_data_id = create_service_data(service_info["team_id"], ProjectConfig.service_id)

    all_files = []
    for path in files_or_dirs:
        if not path.exists():
            print(f"{path} doesn't exist, please specify a valid path")
            raise typer.Exit(code=1)
        if path.is_dir():
            for child_path in path.rglob("*"):
                if child_path.is_file():
                    all_files.append(str(child_path.relative_to(path.parent)))
        else:
            all_files.append(str(path))

    upload_urls = get_service_data_upload_urls(linked_data_id, all_files)
    for file_to_upload, s3_url in upload_urls.items():
        res = upload_file_to_s3(file_to_upload, s3_url)
        if res.status_code != 200:
            print(f"file upload for {file_to_upload} failed, please retry...")


@logged_in_command(data_app, name="ls")
def list_data() -> None:
    """
    Display uploaded data information.
    """
    if ProjectConfig.service_id is None:
        print("Project not initialized yet.")
        raise typer.Exit(code=1)

    linked_data_id = get_linked_service_data(ProjectConfig.service_id)
    if not linked_data_id:
        print("No service data created")
        return

    items = list_service_data_items(linked_data_id)
    if len(items) == 0:
        print("No uploaded data found.")
        return

    table = Table(*DATA_ITEM_HEADER)

    for item in items:
        table.add_row(item["file_name"], item["last_modified"], f"{item['size']:,}")

    CONSOLE.print(table)
