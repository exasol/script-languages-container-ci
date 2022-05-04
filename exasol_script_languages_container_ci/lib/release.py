import logging
import os
from pathlib import Path

import click
from exasol_integration_test_docker_environment.lib.base import luigi_log_config
from exasol_integration_test_docker_environment.lib.config import build_config

from exasol_script_languages_container_ci.lib.ci_build import ci_build
from exasol_script_languages_container_ci.lib.ci_push import ci_push
from exasol_script_languages_container_ci.lib.ci_test import ci_test
from exasol_script_languages_container_ci.lib.github_release_asset_uploader import GithubReleaseAssetUploader
from exasol_script_languages_container_ci.lib.release_upload import release_upload


def release(ctx: click.Context,
            flavor: str,
            branch_name: str,
            docker_user: str,
            docker_password: str,
            docker_release_repository: str,
            config_file: str,
            upload_url: str,
            release_uploader: GithubReleaseAssetUploader):
    """
    Run Release build:
    1. Build image
    2. Run basic tests
    3. Push to docker release repository
    4. Upload to GH release url
    """
    logging.info(f"Running Release build for parameters: {locals()}")

    flavor_path = (f"flavors/{flavor}",)

    log_path = Path(build_config.DEFAULT_OUTPUT_DIRECTORY) / "jobs" / "logs" / "main.log"
    os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME] = f"{log_path.absolute()}"

    ci_build(ctx, flavor_path=flavor_path, rebuild=True, build_docker_repository="",
             commit_sha="", docker_user="", docker_password="")
    ci_test(ctx, flavor_path=flavor_path)
    ci_push(ctx, flavor_path=flavor_path,
            target_docker_repository=docker_release_repository, target_docker_tag_prefix="",
            docker_user=docker_user, docker_password=docker_password)
    release_upload(ctx, flavor_path=flavor_path, upload_url=upload_url, release_uploader=release_uploader)
