import os
from unittest.mock import call, patch, MagicMock

import pytest
from exasol_integration_test_docker_environment.cli.commands.build_test_container import build_test_container
from exasol_script_languages_container_tool.cli.commands import build, run_db_test, push, security_scan

from exasol_script_languages_container_ci.lib.ci import ci

import exasol_script_languages_container_ci

from test.fixtures import tmp_test_dir, click_stub, test_env, patch_printfile


@pytest.fixture(autouse=True)
def last_commit():
    """
    This overwrites automatically function "exasol_script_languages_container_ci.lib.get_last_commit_message" and always
    returns "last commit". Hence we can execute the tests within a none-Git directory.
    """
    with patch('exasol_script_languages_container_ci.lib.get_last_commit_message', MagicMock(return_value="last commit")):
        yield


class TestCI:

    def test_feature_branch_build(self, click_stub, test_env):
        """
        Test that on feature branches we run normal build:
         1. Build Image (no force_rebuild)
         2. Run db tests
         3. Security scan
         4. Push to docker build repo (with and withou sha)
        """
        TEST_BRANCH = "refs/heads/test_feature_branch"

        ci(click_stub, flavor="TEST_FLAVOR", branch_name=TEST_BRANCH,
           docker_user=test_env.docker_user, docker_password=test_env.docker_pwd,
           docker_build_repository=test_env.docker_build_repo,
           docker_release_repository=test_env.docker_release_repo, commit_sha=test_env.commit_sha)

        build_call = call(build, flavor_path=("flavors/TEST_FLAVOR",),
                          force_rebuild=False,
                          source_docker_repository_name=test_env.docker_build_repo,
                          source_docker_username=test_env.docker_user,
                          source_docker_tag_prefix=test_env.commit_sha,
                          source_docker_password=test_env.docker_pwd,
                          shortcut_build=False, workers=7)
        build_test_container_call = call(build_test_container, force_rebuild=False, workers=7)
        run_db_test_call_1 = call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7)
        run_db_test_call_2 = call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7,
                                  test_folder="test/linker_namespace_sanity", release_goal="base_test_build_run")
        security_scan_call = call(security_scan, flavor_path=("flavors/TEST_FLAVOR",), workers=7)
        push_call_1 = call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                           target_docker_repository_name=test_env.docker_build_repo,
                           target_docker_tag_prefix=test_env.commit_sha,
                           target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
        push_call_2 = call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                           target_docker_repository_name=test_env.docker_build_repo,
                           target_docker_tag_prefix="",
                           target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
        assert (click_stub.invoke.mock_calls == [build_call, build_test_container_call,
                                                 run_db_test_call_1, run_db_test_call_2,
                                                 security_scan_call,
                                                 push_call_1, push_call_2])

    def test_feature_rebuild_build(self, click_stub, test_env):
        """
        Test that on branches with prefix "rebuild/" normal build, but with force_rebuild=true
         1. Build Image (with force_rebuild)
         2. Run db tests
         3. Security scan
         4. Push to docker build repo (with and withou sha)
        """
        TEST_BRANCH = "refs/heads/rebuild/test_feature_branch"

        ci(click_stub, flavor="TEST_FLAVOR", branch_name=TEST_BRANCH,
           docker_user=test_env.docker_user, docker_password=test_env.docker_pwd,
           docker_build_repository=test_env.docker_build_repo,
           docker_release_repository=test_env.docker_release_repo, commit_sha=test_env.commit_sha)

        build_call = call(build, flavor_path=("flavors/TEST_FLAVOR",),
                          force_rebuild=True,
                          source_docker_repository_name=test_env.docker_build_repo,
                          source_docker_username=test_env.docker_user,
                          source_docker_tag_prefix=test_env.commit_sha,
                          source_docker_password=test_env.docker_pwd,
                          shortcut_build=False, workers=7)
        build_test_container_call = call(build_test_container, force_rebuild=True, workers=7)
        run_db_test_call_1 = call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7)
        run_db_test_call_2 = call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7,
                                  test_folder="test/linker_namespace_sanity", release_goal="base_test_build_run")
        security_scan_call = call(security_scan, flavor_path=("flavors/TEST_FLAVOR",), workers=7)
        push_call_1 = call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                           target_docker_repository_name=test_env.docker_build_repo,
                           target_docker_tag_prefix=test_env.commit_sha,
                           target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
        push_call_2 = call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                           target_docker_repository_name=test_env.docker_build_repo,
                           target_docker_tag_prefix="",
                           target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
        assert (click_stub.invoke.mock_calls == [build_call, build_test_container_call,
                                                 run_db_test_call_1, run_db_test_call_2,
                                                 security_scan_call,
                                                 push_call_1, push_call_2])

    def test_master_build(self, click_stub, test_env):
        """
        Test that on branch master, we force rebuild and push also to release docker repository
         1. Build Image (with force_rebuild)
         2. Run db tests
         3. Security scan
         4. Push to docker build repo (with and withou sha)
         5. Push to docker release repo
        """
        TEST_BRANCH = "refs/heads/master"

        ci(click_stub, flavor="TEST_FLAVOR", branch_name=TEST_BRANCH,
           docker_user=test_env.docker_user, docker_password=test_env.docker_pwd,
           docker_build_repository=test_env.docker_build_repo,
           docker_release_repository=test_env.docker_release_repo, commit_sha=test_env.commit_sha)
        build_call = call(build, flavor_path=("flavors/TEST_FLAVOR",),
                          force_rebuild=True,
                          source_docker_repository_name=test_env.docker_build_repo,
                          source_docker_username=test_env.docker_user,
                          source_docker_tag_prefix=test_env.commit_sha,
                          source_docker_password=test_env.docker_pwd,
                          shortcut_build=False, workers=7)
        build_test_container_call = call(build_test_container, force_rebuild=True, workers=7)
        run_db_test_call_1 = call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7)
        run_db_test_call_2 = call(run_db_test, flavor_path=("flavors/TEST_FLAVOR",), workers=7,
                                  test_folder="test/linker_namespace_sanity", release_goal="base_test_build_run")
        security_scan_call = call(security_scan, flavor_path=("flavors/TEST_FLAVOR",), workers=7)
        push_call_1 = call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                           target_docker_repository_name=test_env.docker_build_repo,
                           target_docker_tag_prefix=test_env.commit_sha,
                           target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
        push_call_2 = call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                           target_docker_repository_name=test_env.docker_build_repo,
                           target_docker_tag_prefix="",
                           target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
        push_call_3 = call(push, flavor_path=("flavors/TEST_FLAVOR",), push_all=True, force_push=True, workers=7,
                           target_docker_repository_name=test_env.docker_release_repo,
                           target_docker_tag_prefix="",
                           target_docker_username=test_env.docker_user, target_docker_password=test_env.docker_pwd)
        assert (click_stub.invoke.mock_calls == [build_call, build_test_container_call,
                                                 run_db_test_call_1, run_db_test_call_2,
                                                 security_scan_call,
                                                 push_call_1, push_call_2, push_call_3])
