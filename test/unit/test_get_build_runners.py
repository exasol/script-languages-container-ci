import json
from test.unit.test_env import test_env
from unittest.mock import MagicMock

from exasol.slc_ci.lib.get_build_runners import (
    get_build_runners as lib_get_build_runners,
)


def test_get_build_runners(build_config_with_flavor_environment):
    github_output_mock = MagicMock()
    lib_get_build_runners("flavor_a", github_output_mock)
    assert (
        json.loads(github_output_mock.write_result.call_args.args[0])
        == test_env.flavor_ci_config.build_runners
    )
