import os
from pathlib import Path
from unittest import mock

import pytest
from exasol_integration_test_docker_environment.cli.options.system_options import DEFAULT_OUTPUT_DIRECTORY
from exasol_integration_test_docker_environment.lib.base import luigi_log_config

from exasol_script_languages_container_ci.lib.ci_prepare import CIPrepare


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {}):
        yield


def test_ci_prepare_log_environment_variable_is_set():
    CIPrepare().prepare()
    expected_log_path = str(Path(DEFAULT_OUTPUT_DIRECTORY) / "jobs" / "logs" / "main.log")
    assert luigi_log_config.LOG_ENV_VARIABLE_NAME in os.environ \
           and os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME].endswith(expected_log_path)


def test_ci_prepare_log_path_exists():
    CIPrepare().prepare()
    assert Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME]).parent.is_dir()
