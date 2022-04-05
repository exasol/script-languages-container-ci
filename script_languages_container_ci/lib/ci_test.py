import logging
from typing import Tuple

import click
from exasol_script_languages_container_tool.cli.commands import run_db_test

import script_languages_container_ci


def ci_test(ctx: click.Context, flavor_path: Tuple[str, ...]):
    if "skip tests" not in script_languages_container_ci.lib.get_last_commit_message():
        logging.info(f"Running command 'run_db_test' with parameters {locals()}")
        ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7)
        logging.info(f"Running command 'run_db_test' for linker_namespace_sanity with parameters {locals()}")
        ctx.invoke(run_db_test, flavor_path=flavor_path, workers=7,
                   test_folder="test/linker_namespace_sanity", release_goal="base_test_build_run")
        script_languages_container_ci.lib.print_docker_images()
    else:
        logging.warning("Skipping tests.")
