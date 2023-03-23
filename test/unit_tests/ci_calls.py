from unittest.mock import call

from exasol_integration_test_docker_environment.lib.api.build_test_container import build_test_container
from exasol_script_languages_container_tool.cli.commands import build, run_db_test, security_scan, push

from test.unit_tests.test_env import test_env


def build_call(force_rebuild: bool):
    return call.build(flavor_path=("flavors/TEST_FLAVOR",),
                      rebuild=force_rebuild,
                      build_docker_repository=test_env.docker_build_repo,
                      commit_sha=test_env.commit_sha,
                      docker_user=test_env.docker_user,
                      docker_password=test_env.docker_pwd,
                      test_container_folder='test_container')


def run_db_test_call():
    return call.execute_tests(flavor_path=("flavors/TEST_FLAVOR",),
                              docker_user=test_env.docker_user,
                              docker_password=test_env.docker_pwd,
                              test_container_folder='test_container')


def security_scan_call():
    return call.run_security_scan(flavor_path=("flavors/TEST_FLAVOR",))


def push_build_repo_with_sha_call():
    return call.push(flavor_path=("flavors/TEST_FLAVOR",),
                     target_docker_repository=test_env.docker_build_repo,
                     target_docker_tag_prefix=test_env.commit_sha,
                     docker_user=test_env.docker_user,
                     docker_password=test_env.docker_pwd)


def push_build_repo_without_sha_call():
    return call.push(flavor_path=("flavors/TEST_FLAVOR",),
                target_docker_repository=test_env.docker_build_repo,
                target_docker_tag_prefix="",
                docker_user=test_env.docker_user,
                docker_password=test_env.docker_pwd)


def push_release_repo():
    return call.push(flavor_path=("flavors/TEST_FLAVOR",),
                     target_docker_repository=test_env.docker_release_repo,
                     target_docker_tag_prefix="",
                     docker_user=test_env.docker_user,
                     docker_password=test_env.docker_pwd)
