import json
from test.unit.test_env import test_env
from unittest.mock import MagicMock

from exasol.slc_ci.lib.get_test_matrix import get_test_matrix as lib_get_test_matrix

EXPECTED_VALUES = {
    "include": [
        {
            "test-set-name": "all",
            "test-runner": "some_test_runner",
            "goal": "release",
        },
        {
            "test-set-name": "pandas",
            "test-runner": "some_test_runner",
            "goal": "release",
        },
        {
            "test-set-name": "generic",
            "test-runner": "some_test_runner",
            "goal": "release",
        },
        {
            "test-set-name": "gpu",
            "test-runner": "gpu_runner",
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
