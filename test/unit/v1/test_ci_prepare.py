import os
from pathlib import Path
from unittest import mock

import pytest
from exasol_integration_test_docker_environment.cli.options.system_options import (
    DEFAULT_OUTPUT_DIRECTORY,
)
from exasol_integration_test_docker_environment.lib.logging import luigi_log_config

from exasol_script_languages_container_ci.lib.ci_prepare import CIPrepare

EXPECTED_LOG_PARENT_DIRECTORY = Path(DEFAULT_OUTPUT_DIRECTORY) / "jobs" / "logs"
EXPECTED_LOG_FILE = EXPECTED_LOG_PARENT_DIRECTORY / "main.log"


def test_ci_prepare_log_environment_variable_is_set(mock_settings_env_vars):
    CIPrepare().prepare()
    assert luigi_log_config.LOG_ENV_VARIABLE_NAME in os.environ


def test_ci_prepare_log_environment_variable_is_set_to_the_correct_path(
    mock_settings_env_vars,
):
    CIPrepare().prepare()
    expected_path = str(EXPECTED_LOG_FILE.absolute())
    assert os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME] == expected_path


def test_ci_prepare_log_path_parent_directory_doesnt_exists(mock_settings_env_vars):
    CIPrepare().prepare()
    assert Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME]).parent.is_dir()


def test_ci_prepare_log_path_file_doesnt_exist(mock_settings_env_vars):
    CIPrepare().prepare()
    actual_path = Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME])
    assert not actual_path.exists()


def test_ci_prepare_log_path_parent_directory_exist(mock_settings_env_vars):
    EXPECTED_LOG_PARENT_DIRECTORY.mkdir(parents=True)
    CIPrepare().prepare()
    assert (
        Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME]).parent
        == EXPECTED_LOG_PARENT_DIRECTORY.absolute()
    )


def test_ci_prepare_log_path_file_exists(mock_settings_env_vars):
    expected_value = "Test"
    EXPECTED_LOG_PARENT_DIRECTORY.mkdir(parents=True)
    with EXPECTED_LOG_FILE.open("wt") as f:
        f.write(expected_value)
    CIPrepare().prepare()
    actual_path = Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME])
    actual_value = actual_path.read_text()
    assert (
        actual_value == expected_value and actual_path == EXPECTED_LOG_FILE.absolute()
    )
