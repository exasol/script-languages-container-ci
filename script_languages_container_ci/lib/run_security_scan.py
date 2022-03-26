from pathlib import Path

import click
from exasol_script_languages_container_tool.cli.commands import security_scan

from script_languages_container_ci.lib import print_docker_images, print_file


def run_security_scan(ctx: click.Context, flavor: str):
    print(f"Running command 'security_scan' with parameters {locals()} ")
    ctx.invoke(security_scan, flavor=f"flavors/{flavor}", workers=7)
    print_docker_images()
    print("============= SECURITY REPORT ===========")
    print_file(Path() / ".build_output" / "security_scan" / "security_report")
