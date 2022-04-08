import logging
from pathlib import Path
from typing import Tuple

import click
from exasol_script_languages_container_tool.cli.commands import security_scan

import exasol_script_languages_container_ci


def ci_security_scan(ctx: click.Context, flavor_path: Tuple[str, ...]):
    """
    Run security scan and print result
    """

    logging.info(f"Running command 'security_scan' with parameters {locals()}")
    ctx.invoke(security_scan, flavor_path=flavor_path, workers=7)
    exasol_script_languages_container_ci.lib.print_docker_images(logging.info)
    logging.info("============= SECURITY REPORT ===========")
    #Important: Call print_file over the global module name, otherwise the patch in the unit-test does not work!
    exasol_script_languages_container_ci.lib.print_file(
        Path() / ".build_output" / "security_scan" / "security_report", logging.info)
