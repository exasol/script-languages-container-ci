import json
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterable
from inspect import cleandoc

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

    writer(cleandoc("""
        {seperator}
        Printing docker images
        {seperator}
        {images}""").format(
        seperator=20 * "=", images="\n".join(_get_docker_images())
    ))


def get_last_commit_message():
    """
    Assumes that PWD belongs to a GIT repository. Get's the last commit message of this repo and returns it as string
    :return: Last commit message of current working directory GIT repository.
    """
    return Repo().head.commit.message


def print_file(filename: Path, writer: Callable[[str], None]):
    """
    Opens file readonly, reads it content and prints to writer.
    """
    with open(filename, "r") as f:
        writer(f.read())


def get_files_of_last_commit() -> Iterable[str]:
    """
    Returns the files of the last commit of the repo in the cwd.
    """
    repo = Repo()
    commit = repo.head.commit
    return commit.stats.files.keys()


@contextmanager
def get_config(config_file: str):
    """
    Opens config file and returns parsed JSON object.
    """
    with open(config_file, "r") as f:
        yield json.load(f)
