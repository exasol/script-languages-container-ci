from test.unit.github.test_env import test_env
from unittest.mock import MagicMock

from exasol.slc_ci.lib.get_build_runner import get_build_runner as lib_get_build_runner


def test_get_build_runner(build_config_with_flavor_environment):
    github_output_mock = MagicMock()
    lib_get_build_runner("flavor_a", github_output_mock)
    assert (
        github_output_mock.write_result.call_args.args[0]
        == test_env.flavor_ci_config.build_runner
    )
