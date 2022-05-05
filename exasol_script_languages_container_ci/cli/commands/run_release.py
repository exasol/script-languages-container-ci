import logging

import click

from exasol_script_languages_container_ci.cli.cli import cli
from exasol_script_languages_container_ci.lib.github_release_asset_uploader import GithubReleaseAssetUploader
from exasol_script_languages_container_ci.lib.release import release


@cli.command()
@click.option('--flavor', required=True, type=str,
              help="Flavor name.")
@click.option('--docker-user', required=True, type=str,
              help="Docker user name")
@click.option('--docker-password', required=True, type=str,
              help="Docker password")
@click.option('--docker-release-repository', required=True, type=str,
              help="Docker release repository")
@click.option('--config-file', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help="The build config file (project specific)")
@click.option('--repository', required=True, type=str,
              help="The id of the repository.")
@click.option('--release_key', required=True, type=str,
              help="The id or tag of the release.")
@click.option('--dry-run/--no-dry-run', default=False,
              help="If true, runs release without pushing the container to the docker release repository."
                   "If false, also pushes the container to the docker release repository.")
@click.pass_context
def run_release(ctx: click.Context,
                flavor: str,
                docker_user: str,
                docker_password: str,
                docker_release_repository: str,
                config_file: str,
                repository: str,
                release_key: str,
                dry_run: bool):
    logging.basicConfig(level=logging.INFO)
    release(ctx, flavor, docker_user, docker_password,
            docker_release_repository, config_file, repository, release_key, GithubReleaseAssetUploader(), dry_run)
