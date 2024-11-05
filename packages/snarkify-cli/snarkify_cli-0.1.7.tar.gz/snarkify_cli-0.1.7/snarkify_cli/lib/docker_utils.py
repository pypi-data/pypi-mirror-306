import contextlib
import os
from datetime import datetime, timezone
from typing import Optional

import docker
import typer
from rich import print

from snarkify_cli.lib.constants import IMAGE_REGISTRY, KNATIVE_FUNC_IMAGE
from snarkify_cli.templates.build_templates import FUNC_YAML_TEMPLATE, PROCFILE_TEMPLATE


@contextlib.contextmanager
def _create_build_files(service_id: str, base_dir: str):
    with _create_procfile(base_dir), _create_func_yaml(service_id, base_dir):
        yield


@contextlib.contextmanager
def _create_procfile(base_dir: str):
    procfile_path = f"{base_dir}/Procfile"
    with open(procfile_path, "w") as f:
        f.write(PROCFILE_TEMPLATE)
    try:
        yield
    finally:
        os.remove(procfile_path)


@contextlib.contextmanager
def _create_func_yaml(service_id: str, base_dir: str):
    formatted_now = datetime.now(timezone.utc).isoformat()
    image_name = f"{IMAGE_REGISTRY}/{os.path.basename(os.getcwd())}"
    func_yaml_content = FUNC_YAML_TEMPLATE.format(service_id, image_name, formatted_now)

    func_yaml_path = f"{base_dir}/func.yaml"
    with open(func_yaml_path, "w") as f:
        f.write(func_yaml_content)

    try:
        yield
    finally:
        os.remove(func_yaml_path)


def func_build(service_id: str, base_dir: str):
    client = docker.from_env()

    # Ensure the path is absolute
    code_abs_path = os.path.abspath(".")
    base_abs_path = f"{code_abs_path}/{base_dir}"

    # Docker socket file path
    docker_socket = "/var/run/docker.sock"
    # Start the shell and execute the command with stream=True
    with _create_build_files(service_id, base_abs_path):
        shell = client.shells.run(
            KNATIVE_FUNC_IMAGE,
            command="build --registry docker.io/snarkify",
            working_dir=f"/code/{base_dir}",
            volumes={
                code_abs_path: {"bind": "/code", "mode": "rw"},
                docker_socket: {"bind": "/var/run/docker.sock", "mode": "rw"},
            },
            detach=True,
        )

        # Iterate over the output stream and print to standard output
        for line in shell.logs(stream=True, timestamps=True):
            print(line.decode().strip())

        # Wait for the shell to finish and get the exit code
        exit_status = shell.wait()["StatusCode"]

        # Check exit status
        if exit_status != 0:
            print(f"Build process exited with a non-zero exit code {exit_status}.")
            raise typer.Exit(code=1)
        else:
            print("Docker image has successfully been built.")


def save_image(tar_file_path: str, image_name: Optional[str] = None):
    client = docker.from_env()
    if image_name is None:
        image_name = f"{IMAGE_REGISTRY}/{os.path.basename(os.getcwd())}"
    image = client.images.get(image_name)
    image_tar = image.save(named=True)

    with open(tar_file_path, "wb") as file:
        for chunk in image_tar:
            file.write(chunk)
