import json
from test.unit.test_env import test_env
from unittest.mock import MagicMock

from exasol.slc_ci.lib.get_test_matrix import get_test_matrix as lib_get_test_matrix

EXPECTED_VALUES = {
    "include": [
        {
            "test-set-name": "all",
            "test-runner": "ubuntu-22.04",
            "goal": "release",
        },
        {
            "test-set-name": "all",
            "test-runner": "ubuntu-22.04-arm",
            "goal": "release",
        },
        {
            "test-set-name": "pandas_dtype_leak",
            "test-runner": "ubuntu-22.04",
            "goal": "release",
        },
        {
            "test-set-name": "pandas_dtype_leak",
            "test-runner": "ubuntu-22.04-arm",
            "goal": "release",
        },
        {
            "test-set-name": "pandas_dataframe_leak",
            "test-runner": "ubuntu-22.04",
            "goal": "release",
        },
        {
            "test-set-name": "pandas_dataframe_leak",
            "test-runner": "ubuntu-22.04-arm",
            "goal": "release",
        },
        {
            "test-set-name": "pandas",
            "test-runner": "ubuntu-22.04",
            "goal": "release",
        },
        {
            "test-set-name": "pandas",
            "test-runner": "ubuntu-22.04-arm",
            "goal": "release",
        },
        {
            "test-set-name": "generic",
            "test-runner": "ubuntu-22.04",
            "goal": "release",
        },
        {
            "test-set-name": "generic",
            "test-runner": "ubuntu-22.04-arm",
            "goal": "release",
        },
        {
            "test-set-name": "gpu",
            "test-runner": "gpu_test_runner_1",
            "goal": "release",
        },
        {
            "test-set-name": "gpu",
            "test-runner": "gpu_test_runner_2",
            "goal": "release",
        },
    ]
}


def test_get_test_matrix(
    build_config_with_flavor_environment,
):
    github_output_mock = MagicMock()
    lib_get_test_matrix(test_env.flavor_name, github_output_mock)
    assert (
        json.loads(github_output_mock.write_result.call_args.args[0]) == EXPECTED_VALUES
    )
