import logging
import os
import re
from pathlib import Path

import click
from exasol_integration_test_docker_environment.lib.base import luigi_log_config
from exasol_integration_test_docker_environment.lib.config import build_config

import exasol_script_languages_container_ci
from exasol_script_languages_container_ci.lib.common import get_config
from exasol_script_languages_container_ci.lib.ci_build import ci_build
from exasol_script_languages_container_ci.lib.ci_push import ci_push
from exasol_script_languages_container_ci.lib.ci_security_scan import ci_security_scan
from exasol_script_languages_container_ci.lib.ci_test import ci_test


def check_if_need_to_build(config_file: str, flavor: str):
    affected_files = list(exasol_script_languages_container_ci.lib.common.get_files_of_last_commit())
    logging.debug(f"check_if_need_to_build: Found files of last commit: {affected_files}")
    with get_config(config_file) as config:
        for ignore_path in config["build_ignore"]["ignored_paths"]:
            affected_files = list(filter(lambda file: not file.startswith(ignore_path), affected_files))

    if len(affected_files) > 0:
        # Now filter out also other flavor folders
        this_flavor_path = f"flavors/{flavor}"
        affected_files = list(filter(lambda file: not file.startswith("flavors") or file.startswith(this_flavor_path),
                                     affected_files))
    logging.debug(f"check_if_need_to_build: filtered files: {affected_files}")
    return len(affected_files) > 0


def ci(ctx: click.Context,
       flavor: str,
       branch_name: str,
       docker_user: str,
       docker_password: str,
       docker_build_repository: str,
       docker_release_repository: str,
       commit_sha: str,
       config_file: str):
    """
    Run CI build:
    1. Build image
    2. Run db tests
    3. Run security scan
    4. Push to docker repositories
    """
    logging.info(f"Running CI build for parameters: {locals()}")

    rebuild = False
    push_to_public_cache = False

    IS_REBUILD = re.compile(r"refs/heads/rebuild/.*")
    IS_MASTER = re.compile(r"refs/heads/master")

    rebuild = bool(IS_REBUILD.match(branch_name) or IS_MASTER.match(branch_name))
    push_to_public_cache = bool(IS_MASTER.match(branch_name))

    flavor_path = (f"flavors/{flavor}",)

    need_to_run = rebuild or check_if_need_to_build(config_file, flavor)

    if need_to_run:
        log_path = Path(build_config.DEFAULT_OUTPUT_DIRECTORY) / "jobs" / "logs" / "main.log"
        os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME] = f"{log_path.absolute()}"

        ci_build(ctx, flavor_path=flavor_path, rebuild=rebuild, build_docker_repository=docker_build_repository,
                 commit_sha=commit_sha,
                 docker_user=docker_user, docker_password=docker_password)
        ci_test(ctx, flavor_path=flavor_path)
        ci_security_scan(ctx, flavor_path=flavor_path)
        ci_push(ctx, flavor_path=flavor_path,
                target_docker_repository=docker_build_repository, target_docker_tag_prefix=commit_sha,
                docker_user=docker_user, docker_password=docker_password)
        ci_push(ctx, flavor_path=flavor_path,
                target_docker_repository=docker_build_repository, target_docker_tag_prefix="",
                docker_user=docker_user, docker_password=docker_password)

        if push_to_public_cache:
            ci_push(ctx, flavor_path=flavor_path,
                    target_docker_repository=docker_release_repository, target_docker_tag_prefix="",
                    docker_user=docker_user, docker_password=docker_password)
    else:
        logging.warning(f"Skipping build...")
