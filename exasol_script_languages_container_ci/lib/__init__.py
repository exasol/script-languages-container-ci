from pathlib import Path
from typing import Callable

import docker
from git import Repo


def _get_docker_images():
    docker_client = docker.from_env()
    exa_images = []
    try:
        exa_images = [str(img) for img in docker_client.images.list() if "exa" in str(img)]
    finally:
        docker_client.close()
    return exa_images


def print_docker_images(writer: Callable[[str], None]):
    """
    Prints all docker images whith "exa" in it's name to stdout.
    :return: None
    """
    writer(
            """
==========================================================
Printing docker images
==========================================================
"""
    )
    writer(f"{_get_docker_images()}")


def get_last_commit_message():
    """
    Assumes that PWD belongs to a GIT repository. Get's the last commit message of this repo and returns it as string
    :return: Last commit message of current working directory GIT repository.
    """
    repo = Repo()
    return repo.head.commit.message


def print_file(filename: Path, writer: Callable[[str], None]):
    """
    Opens file readonly, reads it content and prints to writer.
    """
    with open(filename, "r") as f:
        content = f.read()
        writer(content)

