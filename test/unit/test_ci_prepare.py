import datetime
import os
from pathlib import Path
from unittest import mock

import pytest
from exasol_integration_test_docker_environment.cli.options.system_options import (
    DEFAULT_OUTPUT_DIRECTORY,
)
from exasol_integration_test_docker_environment.lib.logging import luigi_log_config

from exasol.slc_ci.lib.ci_prepare import CIPrepare

EXPECTED_LOG_PARENT_DIRECTORY = Path(DEFAULT_OUTPUT_DIRECTORY) / "jobs" / "logs"
EXPECTED_LOG_FILE = EXPECTED_LOG_PARENT_DIRECTORY / "main.log"

COMMIT_SHA = "sha_123"


def test_ci_prepare_log_environment_variable_is_set(
    mock_settings_env_vars, tmp_test_dir
):
    CIPrepare().prepare(COMMIT_SHA)
    assert luigi_log_config.LOG_ENV_VARIABLE_NAME in os.environ


def test_ci_prepare_log_environment_variable_is_set_to_the_correct_path(
    mock_settings_env_vars,
    tmp_test_dir,
):
    CIPrepare().prepare(COMMIT_SHA)
    expected_path = str(EXPECTED_LOG_FILE.absolute())
    assert os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME] == expected_path


def test_ci_prepare_log_path_parent_directory_doesnt_exists(
    mock_settings_env_vars, tmp_test_dir
):
    CIPrepare().prepare(COMMIT_SHA)
    assert Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME]).parent.is_dir()


def test_ci_prepare_log_path_file_doesnt_exist(mock_settings_env_vars, tmp_test_dir):
    CIPrepare().prepare(COMMIT_SHA)
    actual_path = Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME])
    assert not actual_path.exists()


def test_ci_prepare_log_path_parent_directory_exist(
    mock_settings_env_vars, tmp_test_dir
):
    EXPECTED_LOG_PARENT_DIRECTORY.mkdir(parents=True)
    CIPrepare().prepare(COMMIT_SHA)
    assert (
        Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME]).parent
        == EXPECTED_LOG_PARENT_DIRECTORY.absolute()
    )


def test_ci_prepare_log_path_file_exists(mock_settings_env_vars, tmp_test_dir):
    expected_value = "Test"
    EXPECTED_LOG_PARENT_DIRECTORY.mkdir(parents=True)
    with EXPECTED_LOG_FILE.open("wt") as f:
        f.write(expected_value)
    CIPrepare().prepare(COMMIT_SHA)
    actual_path = Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME])
    actual_value = actual_path.read_text()
    assert (
        actual_value == expected_value and actual_path == EXPECTED_LOG_FILE.absolute()
    )


def test_ci_prepare_meta_data_dir_exists(mock_settings_env_vars, tmp_test_dir):
    CIPrepare().prepare(COMMIT_SHA)
    OUTPUT_PATH = Path(DEFAULT_OUTPUT_DIRECTORY)
    META_DATA_PATH = OUTPUT_PATH / "meta_data"
    assert META_DATA_PATH.exists() and META_DATA_PATH.is_dir()


def test_ci_prepare_security_scan_dir_exists(mock_settings_env_vars, tmp_test_dir):
    CIPrepare().prepare(COMMIT_SHA)
    OUTPUT_PATH = Path(DEFAULT_OUTPUT_DIRECTORY)
    META_DATA_PATH = OUTPUT_PATH / "security_scan"
    assert META_DATA_PATH.exists() and META_DATA_PATH.is_dir()


def test_ci_prepare_start_date(mock_settings_env_vars, tmp_test_dir):
    CIPrepare().prepare(COMMIT_SHA)
    OUTPUT_PATH = Path(DEFAULT_OUTPUT_DIRECTORY)
    date_path = OUTPUT_PATH / "meta_data" / "start_date"
    date = datetime.datetime.fromisoformat(date_path.read_text())
    delta = datetime.datetime.now() - date
    assert datetime.timedelta(0) <= delta < datetime.timedelta(minutes=5)


def test_ci_prepare_commit_sha(mock_settings_env_vars, tmp_test_dir):
    CIPrepare().prepare(COMMIT_SHA)
    OUTPUT_PATH = Path(DEFAULT_OUTPUT_DIRECTORY)
    commi_sha_path = OUTPUT_PATH / "meta_data" / "commit_sha"
    assert commi_sha_path.read_text() == COMMIT_SHA
