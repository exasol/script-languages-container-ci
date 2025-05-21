from exasol_integration_test_docker_environment.lib.utils.cli_function_decorators import (
    add_options,
)

import exasol.slc_ci.lib.get_test_runner as lib_get_test_runner
from exasol.slc_ci.cli.cli import cli
from exasol.slc_ci.cli.options.flavor_options import flavor_options
from exasol.slc_ci.cli.options.github_options import github_options
from exasol.slc_ci.cli.options.test_options import test_set_options
from exasol.slc_ci.lib.github_access import GithubAccess


@cli.command()
@add_options(flavor_options)
@add_options(test_set_options)
@add_options(github_options)
def get_test_runner(flavor: str, test_set_name: str, github_output_var: str):
    github_access = GithubAccess(github_output_var)
    lib_get_test_runner.get_test_runner(
        flavor=flavor, test_set_name=test_set_name, github_access=github_access
    )
