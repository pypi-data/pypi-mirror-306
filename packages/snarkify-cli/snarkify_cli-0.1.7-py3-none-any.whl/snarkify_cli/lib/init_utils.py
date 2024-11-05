import os
import subprocess

from rich import print as rich_print

from snarkify_cli.lib.constants import (
    CARGO_TOML_FILE,
    RUST_PROJECT_TEMPLATE_FILE,
    RUST_PROJECT_TEMPLATE_PATH,
    SERDE_CARGO_LIB,
    SERDE_FEATURES,
    SNARKIFY_RUST_SDK,
    ASYNC_TRAIT_LIB,
)
from snarkify_cli.templates.rust.snarkify_template import RUST_PROJECT_TEMPLATE


def create_rust_project_template():
    os.makedirs(RUST_PROJECT_TEMPLATE_PATH, exist_ok=True)
    file_path = f"{RUST_PROJECT_TEMPLATE_PATH}/{RUST_PROJECT_TEMPLATE_FILE}"
    # Check if the file already exists
    if os.path.exists(file_path):
        rich_print("Project is already initilized.")
    else:
        # Open the file in write mode and write data
        with open(file_path, "w") as file:
            file.write(RUST_PROJECT_TEMPLATE)
        rich_print(f"Template file created at {file_path}")


def add_rust_dependency():
    # Check if func.yaml exists in the current directory
    if not os.path.exists(CARGO_TOML_FILE):
        rich_print("Cargo.toml not found. Skipping dependency update.")
        return
    try:
        # Run cargo add command
        subprocess.run(["cargo", "add", SNARKIFY_RUST_SDK], check=True)
        rich_print(f"Successfully added dependency: {SNARKIFY_RUST_SDK}")
        subprocess.run(["cargo", "add", SERDE_CARGO_LIB, "--features", SERDE_FEATURES], check=True)
        rich_print(f"Successfully added dependency: {SERDE_CARGO_LIB}")
        subprocess.run(["cargo", "add", ASYNC_TRAIT_LIB], check=True)
        rich_print(f"Successfully added dependency: {ASYNC_TRAIT_LIB}")
    except subprocess.CalledProcessError as e:
        rich_print(f"Fail to update Snarkify dependency: {e}")
