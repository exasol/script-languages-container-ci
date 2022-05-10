import logging
from typing import Tuple

import click
from exasol_script_languages_container_tool.cli.commands import run_db_test

from exasol_script_languages_container_ci.lib.branch_config import BranchConfig
from exasol_script_languages_container_ci.lib.common import print_docker_images
from exasol_script_languages_container_ci.lib.git_access import GitAccess


def _need_to_run_tests(branch_name: str, git_access: GitAccess):
    return BranchConfig.test_always(branch_name) or "skip tests" not in git_access.get_last_commit_message()


def execute_test(ctx: click.Context, flavor_path: Tuple[str, ...]):
    """
    Run db tests
    """
    logging.info(f"Running command 'run_db_test' with parameters {locals()}")
    ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7)
    logging.info(f"Running command 'run_db_test' for linker_namespace_sanity with parameters {locals()}")
    ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7,
               test_folder=("test/linker_namespace_sanity",), release_goal=("base_test_build_run",))
    print_docker_images(logging.info)


def ci_test(ctx: click.Context, flavor_path: Tuple[str, ...], branch_name: str, git_access: GitAccess):
    if _need_to_run_tests(branch_name, git_access):
        execute_test(ctx, flavor_path)
    else:
        logging.warning("Skipping tests.")
