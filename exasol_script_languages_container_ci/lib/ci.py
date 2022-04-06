import logging
import re

import click

from exasol_script_languages_container_ci.lib.ci_build import ci_build
from exasol_script_languages_container_ci.lib.ci_push import ci_push
from exasol_script_languages_container_ci.lib.ci_security_scan import ci_security_scan
from exasol_script_languages_container_ci.lib.ci_test import ci_test


def ci(ctx: click.Context,
       flavor: str,
       branch_name: str,
       docker_user: str,
       docker_password: str,
       docker_build_repository: str,
       docker_release_repository: str,
       commit_sha: str):
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
