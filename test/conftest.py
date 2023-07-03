import json
import logging
import os
from inspect import cleandoc
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import pytest

from exasol_script_languages_container_ci.lib.config.config_data_model import Config, Build, Ignore, Release
from exasol_script_languages_container_ci.lib.config.data_model_generator import config_data_model_default_output_file, \
    regenerate_config_data_model

script_path = Path(__file__).absolute().parent

DISABLE_PYDANTIC_MODEL_GENERATION = "--disable-pydantic-model-generation"

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        DISABLE_PYDANTIC_MODEL_GENERATION, action="store_true", default=False,
        help="Disables the generation of the pydantic models from the json schemas"
    )


def pytest_configure(config):
    """
    Some of our tests are based on the pydantic model. We need to make sure, the tests work with the newest
    version. However, we also need regenerate the file as early as possible, before other modules import it.
    For that reason. we are triggering the regeneration in conftest.
    """

    if not config.getoption(DISABLE_PYDANTIC_MODEL_GENERATION):
        output_file = config_data_model_default_output_file()
        regenerate_config_data_model(output_file)
    else:
        logger.warning("Generation of pydantic models from json schema disabled")


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
def build_config() -> Config:
    return Config(
        build=Build(
            ignore=Ignore(paths=["doc"]),
            base_branch="master"),
        release=Release(timeout_in_minutes=1))


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


@pytest.fixture
def expected_json_config() -> str:
    json = cleandoc("""
    {
        "build": {
            "ignore": {
                "paths": [
                    "a/b/c",
                    "e/f/g"
                ]
            },
            "base_branch": ""
        },
        "release": {
            "timeout_in_minutes": 1
        }
    }""")
    return json
