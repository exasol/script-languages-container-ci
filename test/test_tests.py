import os
from unittest.mock import call, MagicMock, patch

from exasol_integration_test_docker_environment.cli.commands.build_test_container import build_test_container
from exasol_script_languages_container_tool.cli.commands import build, run_db_test, push, security_scan

from exasol_script_languages_container_ci.lib.ci import ci

from test.fixtures import build_output_dir, click_stub, test_env


class TestTests:
    @patch('exasol_script_languages_container_ci.lib.get_last_commit_message', MagicMock(return_value="Please be so kind and skip tests!"))
    def test_skip_tests(self, click_stub, build_output_dir, test_env):
        """
        Test that db_tests are not executed if the last commit message contains the words "skip tests"
        """
        os.chdir(build_output_dir)
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
                                                 security_scan_call,
                                                 push_call_1, push_call_2])
