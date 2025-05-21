from test.unit.github.test_env import test_env
from unittest.mock import MagicMock

import pytest

from exasol.slc_ci.lib.get_test_runner import get_test_runner as lib_get_test_runner

TEST_DATA = [t.dict().values() for t in test_env.flavor_ci_config.test_config.test_sets]


@pytest.mark.parametrize(
    "name, folders, goal, generic_language_tests, test_runner", TEST_DATA
)
def test_get_default_test_runner(
    build_config_with_flavor_environment,
    name,
    folders,
    goal,
    generic_language_tests,
    test_runner,
):
    github_output_mock = MagicMock()
    lib_get_test_runner(test_env.flavor_name, name, github_output_mock)
    expected_runner = (
        test_runner
        if test_runner
        else test_env.flavor_ci_config.test_config.default_test_runner
    )
    assert github_output_mock.write_result.call_args.args[0] == expected_runner
