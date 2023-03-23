import json
import os
from dataclasses import dataclass

from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch, MagicMock

import click
import pytest


@pytest.fixture(autouse=True)
def tmp_test_dir():
    """
    Change cwd to a tmp directory for executing tests. Thus, we avoid any possible interference (git repository).
    :return:
    """
    with TemporaryDirectory() as temp_dir:
        old_dir = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(old_dir)

@pytest.fixture
def config_file(tmp_path_factory):
    config_file_path = tmp_path_factory.mktemp("config") / "build_config.json"
    config = {"build_ignore": {"ignored_paths": ["doc"]}, "base_branch": "master"}
    with open(config_file_path, "w") as f:
        json.dump(config, f)
    return config_file_path


@pytest.fixture(autouse=True)
def patch_printfile():
    """
    This overwrites automatically function "exasol_script_languages_container_ci.lib.print_file" because within the UnitTests
    the output files are not being created. Also accelerate Unit-Tests by avoiding file-access.
    """
    with patch('exasol_script_languages_container_ci.lib.common.print_file', MagicMock()):
        yield


@pytest.fixture()
def git_access_mock():
    """
    Return an object which mocks the git access class. The mock object returns some default values useful for the tests.
    """
    git_access_mock = MagicMock()
    git_access_mock.get_last_commits.return_value = ["456", "123"]
    git_access_mock.get_head_commit_sha_of_branch.return_value = "123"
    git_access_mock.get_files_of_commit.return_value = ["src/udfclient.cpp"]
    git_access_mock.get_last_commit_message.return_value = "last commit"
    return git_access_mock


@dataclass
class DockerConfig:
    docker_user: str
    docker_password: str
    docker_build_repository: str
    docker_release_repository: str


@pytest.fixture()
def docker_config() -> DockerConfig:
    config = DockerConfig(
        docker_user=os.environ["DOCKER_USER"],
        docker_password=os.environ["DOCKER_PASSWORD"],
        docker_build_repository=os.environ["DOCKER_BUILD_REPOSITORY"],
        docker_release_repository=os.environ["DOCKER_RELEASE_REPOSITORY"]
    )
    return config
