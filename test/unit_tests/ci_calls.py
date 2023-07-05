from unittest.mock import call

from test.unit_tests.test_env import test_env


def prepare():
    return call.prepare()


def build_ci_call(force_rebuild: bool):
    return call.build(flavor_path=("flavors/TEST_FLAVOR",),
                      rebuild=force_rebuild,
                      build_docker_repository=test_env.docker_build_repo,
                      commit_sha=test_env.commit_sha,
                      docker_user=test_env.docker_user,
                      docker_password=test_env.docker_pwd,
                      test_container_folder='test_container')

def build_release_call():
    return call.build(flavor_path=("flavors/TEST_FLAVOR",),
                      rebuild=True,
                      build_docker_repository=None,
                      commit_sha="",
                      docker_user=None,
                      docker_password=None,
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


def release_upload():
    return call.release_upload(flavor_path=('flavors/TEST_FLAVOR',),
                               source_repo_url='https://github.com/test_source_repo_url',
                               release_id=123)
