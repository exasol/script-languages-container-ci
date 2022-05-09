from unittest.mock import patch, MagicMock

import pytest

from exasol_script_languages_container_ci.lib.ci import ci

from test import exaslct_calls

from test.fixtures import tmp_test_dir, click_stub, patch_printfile, git_access_mock, config_file
from test.test_env import test_env


#Testdata contain tuples of (branch, list(calls to exaslct))
#The goal is to test that for specific branches the correct list of calls (with expected arguments) is passed to exaslct
testdata = [
    ("refs/heads/feature/test_branch", [exaslct_calls.build_call(force_rebuild=False),
                                        exaslct_calls.build_test_container_call(force_rebuild=False),
                                        exaslct_calls.run_db_test_call(),
                                        exaslct_calls.run_db_test_call_for_linker_namespace(),
                                        exaslct_calls.security_scan_call(),
                                        exaslct_calls.push_build_repo_with_sha_call(),
                                        exaslct_calls.push_build_repo_without_sha_call()]
     ),
    ("refs/heads/rebuild/feature/test_branch", [exaslct_calls.build_call(force_rebuild=True),
                                                exaslct_calls.build_test_container_call(force_rebuild=True),
                                                exaslct_calls.run_db_test_call(),
                                                exaslct_calls.run_db_test_call_for_linker_namespace(),
                                                exaslct_calls.security_scan_call(),
                                                exaslct_calls.push_build_repo_with_sha_call(),
                                                exaslct_calls.push_build_repo_without_sha_call()]
     ),
    ("refs/heads/master", [exaslct_calls.build_call(force_rebuild=True),
                           exaslct_calls.build_test_container_call(force_rebuild=True),
                           exaslct_calls.run_db_test_call(),
                           exaslct_calls.run_db_test_call_for_linker_namespace(),
                           exaslct_calls.security_scan_call(),
                           exaslct_calls.push_build_repo_with_sha_call(),
                           exaslct_calls.push_build_repo_without_sha_call(),
                           exaslct_calls.push_release_repo()
                           ]
     )

]


@pytest.mark.parametrize("branch,expected_calls", testdata)
def test_branches(branch, git_access_mock, expected_calls, click_stub, config_file):
    """
    Test that on for specific branches the correct steps are executed:
     1. Build Image (force_rebuild = true/false)
     2. Run db tests
     3. Security scan
     4. Push to docker build repo (with and without sha)
     5. Optionally: Push to docker release repo
    """
    ci(click_stub, flavor="TEST_FLAVOR", branch_name=branch,
       docker_user=test_env.docker_user, docker_password=test_env.docker_pwd,
       docker_build_repository=test_env.docker_build_repo,
       docker_release_repository=test_env.docker_release_repo, commit_sha=test_env.commit_sha,
       config_file=config_file, git_access=git_access_mock)
    assert (click_stub.invoke.mock_calls == expected_calls)
