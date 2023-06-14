import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import pytest

script_path = Path(__file__).absolute().parent


@pytest.fixture
def resources_path() -> Path:
    return script_path / "integration_tests/resources"


@pytest.fixture
def flavors_path(resources_path: Path) -> Path:
    return resources_path / "flavors"


@pytest.fixture
def test_containers_folder(resources_path: Path) -> Path:
    return resources_path / "test_containers"


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
