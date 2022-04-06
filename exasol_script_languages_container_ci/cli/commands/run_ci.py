import logging

import click

from exasol_script_languages_container_ci.cli.cli import cli
from exasol_script_languages_container_ci.lib.ci import ci


@cli.command()
@click.option('--flavor', required=True, type=str,
              help="Flavor name.")
@click.option('--branch-name', required=True, type=str,
              help="Branch name.")
@click.option('--docker-user', required=True, type=str,
              help="Docker user name")
@click.option('--docker-password', required=True, type=str,
              help="Docker password")
@click.option('--docker-build-repository', required=True, type=str,
              help="Docker build repository")
@click.option('--docker-release-repository', required=True, type=str,
              help="Docker release repository")
@click.option('--commit-sha', required=True, type=str,
              help="Commit SHA")
@click.pass_context
def run_ci(ctx: click.Context,
           flavor: str,
           branch_name: str,
           docker_user: str,
           docker_password: str,
           docker_build_repository: str,
           docker_release_repository: str,
           commit_sha: str):
    logging.basicConfig(level=logging.INFO)
    ci(ctx, flavor, branch_name, docker_user, docker_password,
       docker_build_repository, docker_release_repository, commit_sha)