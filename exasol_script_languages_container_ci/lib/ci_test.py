import logging
from typing import Tuple

import click
from exasol_script_languages_container_tool.cli.commands import run_db_test

from exasol_script_languages_container_ci.lib.common import print_docker_images


def execute_tests(ctx: click.Context, flavor_path: Tuple[str, ...], docker_user: str, docker_password: str):
    """
    Run db tests
    """
    logging.info(f"Running command 'run_db_test' for flavor-path {flavor_path}")
    ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7, source_docker_username=docker_user,
               source_docker_password=docker_password)
    logging.info(f"Running command 'run_db_test' for linker_namespace_sanity for flavor-path {flavor_path}")
    ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7,
               test_folder=("test/linker_namespace_sanity",), release_goal=("base_test_build_run",),
               source_docker_username=docker_user, source_docker_password=docker_password)
    print_docker_images(logging.info)
