import re

import click

from script_languages_container_ci.lib.ci_build import ci_build
from script_languages_container_ci.lib.ci_push import ci_push
from script_languages_container_ci.lib.ci_security_scan import ci_security_scan
from script_languages_container_ci.lib.ci_test import ci_test


def ci(ctx: click.Context,
       flavor: str,
       branch_name: str,
       docker_user: str,
       docker_password: str,
       docker_build_repository: str,
       docker_release_repository: str,
       commit_sha: str):
    print(f"Running CI build for parameters: {locals()}")

    rebuild = False
    push_to_public_cache = False

    if re.match(r"refs/heads/rebuild/.*", branch_name):
        rebuild = True
    elif re.match(r"refs/heads/master", branch_name):
        rebuild = True
        push_to_public_cache = True
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
