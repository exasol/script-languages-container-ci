import logging
from pathlib import Path

import docker
from git import Repo


def print_docker_images():
    """
    Prints all docker images whith "exa" in it's name to stdout.
    :return: None
    """
    docker_client = docker.from_env()
    exa_images = [img for img in docker_client.images.list() if "exa" in str(img)]
    logging.info(
            """
==========================================================
Printing docker images
==========================================================
"""
    )
    for exa_img in exa_images:
        logging.info(exa_img)
    docker_client.close()


def get_last_commit_message():
    """
    Assumes that PWD belongs to a GIT repository. Get's the last commit message of this repo and returns it as string
    :return: Last commit message of current working directory GIT repository.
    """
    repo = Repo()
    return repo.head.commit.message


def print_file(filename: Path):
    """
    Opens file readonly, reads it content and prints to stdout
    :param filename: Path of file to print content
    :return: None
    """
    with open(filename, "r") as f:
        content = f.read()
        logging.info(content)

