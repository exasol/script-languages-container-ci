import re

import click

from script_languages_container_ci import cli
from script_languages_container_ci.lib.run_build import run_build
from script_languages_container_ci.lib.run_push import run_push
from script_languages_container_ci.lib.run_test import run_test


@cli.command()
@click.option('--flavor', required=True, type="str",
              help="Flavor name.")
@click.option('--branch-name', required=True, type="str",
              help="Branch name.")
@click.option('--docker-user', required=True, type="str",
              help="Docker user name")
@click.option('--docker-build-repository', required=True, type="str",
              help="Docker build repository")
@click.option('--docker-release-repository', required=True, type="str",
              help="Docker release repository")
@click.option('--commit-sha', required=True, type="str",
              help="Commit SHA")
def run_ci(flavor: str,
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
    elif re.match(r"refs/heads/master/.*", branch_name):
        rebuild = True
        push_to_public_cache = True
    run_build(flavor=flavor, rebuild=rebuild, build_docker_repository=docker_build_repository, commit_sha=commit_sha,
              docker_user=docker_user, docker_password=docker_password)

    run_test(flavor=flavor)
    run_push(flavor=flavor,
             target_docker_repository=docker_build_repository, target_docker_tag_prefix=commit_sha,
             docker_user=docker_user, docker_password=docker_password)
    run_push(flavor=flavor,
             target_docker_repository=docker_build_repository, target_docker_tag_prefix="",
             docker_user=docker_user, docker_password=docker_password)

    if push_to_public_cache:
        run_push(flavor=flavor,
                 target_docker_repository=docker_release_repository, target_docker_tag_prefix="",
                 docker_user=docker_user, docker_password=docker_password)