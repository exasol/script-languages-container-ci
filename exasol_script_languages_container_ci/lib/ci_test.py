import logging
from typing import Tuple

import click
from exasol_script_languages_container_tool.cli.commands import run_db_test

import exasol_script_languages_container_ci
from exasol_script_languages_container_ci.lib import print_docker_images


def ci_test(ctx: click.Context, flavor_path: Tuple[str, ...]):
    """
    Run db tests
    """

    if "skip tests" not in exasol_script_languages_container_ci.lib.get_last_commit_message():
        #logging.info(f"Running command 'run_db_test' with parameters {locals()}")
        #ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7)
        logging.info(f"Running command 'run_db_test' for linker_namespace_sanity with parameters {locals()}")
        ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7,
                   test_folder=("test/linker_namespace_sanity",), release_goal="base_test_build_run")
        print_docker_images(logging.info)
    else:
        logging.warning("Skipping tests.")
