import logging

import click

from exasol_script_languages_container_ci.cli.cli import cli
from exasol_script_languages_container_ci.lib.ci import ci
from exasol_script_languages_container_ci.lib.github_release_asset_uploader import GithubReleaseAssetUploader
from exasol_script_languages_container_ci.lib.release import release


@cli.command()
@click.option('--flavor', required=True, type=str,
              help="Flavor name.")
@click.option('--branch-name', required=True, type=str,
              help="Branch name.")
@click.option('--docker-user', required=True, type=str,
              help="Docker user name")
@click.option('--docker-password', required=True, type=str,
              help="Docker password")
@click.option('--docker-release-repository', required=True, type=str,
              help="Docker release repository")
@click.option('--config-file', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help="The build config file (project specific)")
@click.option('--upload-url', required=True, type=str,
              help="The url where the container tar archives will be uploaded")
@click.pass_context
def run_release(ctx: click.Context,
                flavor: str,
                branch_name: str,
                docker_user: str,
                docker_password: str,
                docker_release_repository: str,
                config_file: str,
                upload_url: str):
    logging.basicConfig(level=logging.INFO)
    release(ctx, flavor, branch_name, docker_user, docker_password,
            docker_release_repository, config_file, upload_url, GithubReleaseAssetUploader())
