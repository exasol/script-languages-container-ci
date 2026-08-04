from collections.abc import Iterator
from pathlib import Path

import docker
import pytest

DEFAULT_SLC_REPOSITORY = "exasol/script-language-container"
TEST_REPOSITORY_PREFIXES = ("test_", "input_docker_")


def _is_test_image_tag(tag: str, flavor_names: set[str]) -> bool:
    repository, separator, image_tag = tag.rpartition(":")
    if not separator:
        return False

    if repository == DEFAULT_SLC_REPOSITORY:
        return any(
            image_tag.startswith(f"{flavor_name}-") for flavor_name in flavor_names
        )

    repository_name = repository.rsplit("/", 1)[-1]
    return repository_name.startswith(TEST_REPOSITORY_PREFIXES)


def _clean_test_images(flavor_names: set[str]) -> None:
    docker_client = docker.from_env()
    try:
        while tags := {
            tag
            for image in docker_client.images.list(all=True)
            for tag in image.tags
            if _is_test_image_tag(tag, flavor_names)
        }:
            removed_tag = False
            last_error = None
            for tag in tags:
                try:
                    docker_client.images.remove(tag, force=True)
                    removed_tag = True
                except docker.errors.ImageNotFound:
                    removed_tag = True
                except docker.errors.APIError as error:
                    last_error = error
            if not removed_tag:
                raise last_error or RuntimeError(
                    "Could not remove integration-test images"
                )
    finally:
        docker_client.close()


@pytest.fixture(autouse=True)
def clean_docker_images(flavors_path: Path) -> Iterator[None]:
    flavor_names = {path.name for path in flavors_path.iterdir() if path.is_dir()}
    _clean_test_images(flavor_names)
    yield
    _clean_test_images(flavor_names)
