import json
from contextlib import contextmanager
from pathlib import Path
from typing import Callable
from inspect import cleandoc

import docker


def _get_docker_images():
    docker_client = docker.from_env()
    exa_images = []
    try:
        exa_images = [str(img) for img in docker_client.images.list() if "exasol" in str(img)]
    finally:
        docker_client.close()
    return exa_images


@contextmanager
def get_config(config_file: str):
    """
    Opens config file and returns parsed JSON object.
    """
    with open(config_file, "r") as f:
        yield json.load(f)
