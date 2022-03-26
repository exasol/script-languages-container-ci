import click
from exasol_integration_test_docker_environment.cli.commands.build_test_container import build_test_container
from exasol_script_languages_container_tool.cli.commands import build

from script_languages_container_ci.lib import print_docker_images


def run_build(ctx: click.Context,
              flavor: str,
              rebuild: bool,
              build_docker_repository: str,
              commit_sha: str,
              docker_user: str,
              docker_password: str):
    print(f"Running command 'build' with parameters: {locals()} ")
    ctx.invoke(build, flavor_path=flavor, force_rebuild=rebuild, source_docker_repository_name=build_docker_repository,
               source_docker_username=docker_user, source_docker_tag_prefix=commit_sha,
               source_docker_password=docker_password, shortcut_build=False, workers=7)
    print(f"Running command 'build_test_container' with parameters: {locals()} ")
    ctx.invoke(build_test_container, force_rebuild=rebuild, workers=7)
    print_docker_images()
