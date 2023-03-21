from unittest.mock import call

from exasol_integration_test_docker_environment.lib.api.build_test_container import build_test_container
from exasol_script_languages_container_tool.cli.commands import build, run_db_test, security_scan, push

from test.test_env import test_env


def build_call(force_rebuild: bool):
    return call(build, flavor_path=("flavors/TEST_FLAVOR",),
                force_rebuild=force_rebuild,
                source_docker_repository_name=test_env.docker_build_repo,
                source_docker_username=test_env.docker_user,
                source_docker_tag_prefix=test_env.commit_sha,
                source_docker_password=test_env.docker_pwd,
                shortcut_build=False, workers=7)


def build_test_container_call(force_rebuild: bool):
    return call(build_test_container, force_rebuild=force_rebuild, workers=7)


def run_db_test_call():
    return call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7,
                source_docker_username=test_env.docker_user, source_docker_password=test_env.docker_pwd)


def run_db_test_call_for_linker_namespace():
    return call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7,
                test_folder=("test/linker_namespace_sanity",), release_goal=("base_test_build_run",),
                source_docker_username=test_env.docker_user, source_docker_password=test_env.docker_pwd)


def security_scan_call():
    return call(security_scan, flavor_path=("flavors/TEST_FLAVOR",), workers=7)


def push_build_repo_with_sha_call():
    return call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                target_docker_repository_name=test_env.docker_build_repo,
                target_docker_tag_prefix=test_env.commit_sha,
                target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)


def push_build_repo_without_sha_call():
    return call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                target_docker_repository_name=test_env.docker_build_repo,
                target_docker_tag_prefix="",
                target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)


def push_release_repo():
    return call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                target_docker_repository_name=test_env.docker_release_repo,
                target_docker_tag_prefix="",
                target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
