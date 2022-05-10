from unittest.mock import MagicMock, patch

import pytest

from exasol_script_languages_container_ci.lib.ci import ci
from test import exaslct_calls

from test.fixtures import tmp_test_dir, click_stub, patch_printfile, config_file, git_access_mock
from test.test_env import test_env

# Testdata contain tuples of (commit_msg, branch_name, list(calls to exaslct))
# The goal is to test that for specific commit messages the correct list of calls (with expected arguments) is passed to exaslct
testdata = [
    #Feature branch should not skip tests if "skip tests" is not in commit message
    ("last commit", "refs/heads/feature_branch", [exaslct_calls.build_call(force_rebuild=False),
                                                  exaslct_calls.build_test_container_call(force_rebuild=False),
                                                  exaslct_calls.run_db_test_call(),
                                                  exaslct_calls.run_db_test_call_for_linker_namespace(),
                                                  exaslct_calls.security_scan_call(),
                                                  exaslct_calls.push_build_repo_with_sha_call(),
                                                  exaslct_calls.push_build_repo_without_sha_call()]
     ),
    #Feature branch should skip tests if "skip tests" is in commit message
    ("Please be so kind and skip tests!", "refs/heads/feature_branch", [exaslct_calls.build_call(force_rebuild=False),
                                                                        exaslct_calls.build_test_container_call(
                                                                            force_rebuild=False),
                                                                        exaslct_calls.security_scan_call(),
                                                                        exaslct_calls.push_build_repo_with_sha_call(),
                                                                        exaslct_calls.push_build_repo_without_sha_call()]
     ),
    #Master branch should execute tests even with skip tests in commit message
    ("Please be so kind and skip tests!", "refs/heads/master", [exaslct_calls.build_call(force_rebuild=True),
                                                                exaslct_calls.build_test_container_call(
                                                                    force_rebuild=True),
                                                                exaslct_calls.run_db_test_call(),
                                                                exaslct_calls.run_db_test_call_for_linker_namespace(),
                                                                exaslct_calls.security_scan_call(),
                                                                exaslct_calls.push_build_repo_with_sha_call(),
                                                                exaslct_calls.push_build_repo_without_sha_call(),
                                                                exaslct_calls.push_release_repo()]
     ),
    #Main branch should execute tests even with skip tests in commit message
    ("Please be so kind and skip tests!", "refs/heads/main", [exaslct_calls.build_call(force_rebuild=True),
                                                              exaslct_calls.build_test_container_call(
                                                                  force_rebuild=True),
                                                              exaslct_calls.run_db_test_call(),
                                                              exaslct_calls.run_db_test_call_for_linker_namespace(),
                                                              exaslct_calls.security_scan_call(),
                                                              exaslct_calls.push_build_repo_with_sha_call(),
                                                              exaslct_calls.push_build_repo_without_sha_call(),
                                                              exaslct_calls.push_release_repo()]
     ),
    #Develop branch should execute tests even with skip tests in commit message
    ("Please be so kind and skip tests!", "refs/heads/develop", [exaslct_calls.build_call(force_rebuild=True),
                                                                 exaslct_calls.build_test_container_call(
                                                                     force_rebuild=True),
                                                                 exaslct_calls.run_db_test_call(),
                                                                 exaslct_calls.run_db_test_call_for_linker_namespace(),
                                                                 exaslct_calls.security_scan_call(),
                                                                 exaslct_calls.push_build_repo_with_sha_call(),
                                                                 exaslct_calls.push_build_repo_without_sha_call()]
     ),

]


@pytest.mark.parametrize("commit_msg,branch_name, expected_calls", testdata)
def test_commit_messages(commit_msg, branch_name, git_access_mock, expected_calls, click_stub, config_file):
    """
    Test that on for specific commit messages the correct steps are executed:
     1. Build Image
     2. Run db tests OR NOT!
     3. Security scan
     4. Push to docker build repo (with and without sha)
     5. Push to docker release repo (if master/main)
    """
    git_access_mock.get_last_commit_message.return_value = commit_msg
    ci(click_stub, flavor="TEST_FLAVOR", branch_name=branch_name,
       docker_user=test_env.docker_user, docker_password=test_env.docker_pwd,
       docker_build_repository=test_env.docker_build_repo,
       docker_release_repository=test_env.docker_release_repo, commit_sha=test_env.commit_sha,
       config_file=config_file, git_access=git_access_mock)
    assert (click_stub.invoke.mock_calls == expected_calls)
