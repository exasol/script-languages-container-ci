from typing import Union
from unittest.mock import create_autospec, MagicMock, Mock

import pytest

from exasol_script_languages_container_ci.lib.ci import ci
from exasol_script_languages_container_ci.lib.ci_build import CIBuild
from exasol_script_languages_container_ci.lib.ci_push import CIPush
from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest

from test.unit_tests import exaslct_calls, ci_calls

from test.unit_tests.test_env import test_env

# Testdata contain tuples of (branch, list(calls to CICommands))
# The goal is to test that for specific branches the correct list of calls (with expected arguments) is passed to the CICommands
testdata_ci = [
    ("refs/heads/feature/test_branch", [ci_calls.build_ci_call(force_rebuild=False),
                                        ci_calls.run_db_test_call(),
                                        ci_calls.security_scan_call(),
                                        ci_calls.push_build_repo_with_sha_call(),
                                        ci_calls.push_build_repo_without_sha_call()]
     ),
    ("refs/heads/rebuild/feature/test_branch", [ci_calls.build_ci_call(force_rebuild=True),
                                                ci_calls.run_db_test_call(),
                                                ci_calls.security_scan_call(),
                                                ci_calls.push_build_repo_with_sha_call(),
                                                ci_calls.push_build_repo_without_sha_call()]
     ),
    ("refs/heads/master", [ci_calls.build_ci_call(force_rebuild=True),
                           ci_calls.run_db_test_call(),
                           ci_calls.security_scan_call(),
                           ci_calls.push_build_repo_with_sha_call(),
                           ci_calls.push_build_repo_without_sha_call(),
                           ci_calls.push_release_repo()
                           ]
     ),
    ("refs/heads/main", [ci_calls.build_ci_call(force_rebuild=True),
                         ci_calls.run_db_test_call(),
                         ci_calls.security_scan_call(),
                         ci_calls.push_build_repo_with_sha_call(),
                         ci_calls.push_build_repo_without_sha_call(),
                         ci_calls.push_release_repo()
                         ]
     ),
    ("refs/heads/develop", [ci_calls.build_ci_call(force_rebuild=True),
                            ci_calls.run_db_test_call(),
                            ci_calls.security_scan_call(),
                            ci_calls.push_build_repo_with_sha_call(),
                            ci_calls.push_build_repo_without_sha_call()
                            ]
     ),

]


@pytest.mark.parametrize("branch,expected_calls", testdata_ci)
def test_branches(branch, git_access_mock, expected_calls, config_file):
    """
    Test that on for specific branches the correct steps are executed:
     1. Build Image (force_rebuild = true/false)
     2. Run db tests
     3. Security scan
     4. Push to docker build repo (with and without sha)
     5. Optionally: Push to docker release repo
    """
    ci_commands_mock: Union[CIBuild, CIPush, CIExecuteTest, CISecurityScan, Mock] = Mock()
    ci(flavor="TEST_FLAVOR",
       branch_name=branch,
       docker_user=test_env.docker_user,
       docker_password=test_env.docker_pwd,
       docker_build_repository=test_env.docker_build_repo,
       docker_release_repository=test_env.docker_release_repo,
       commit_sha=test_env.commit_sha,
       config_file=config_file,
       git_access=git_access_mock,
       ci_build=ci_commands_mock,
       ci_push=ci_commands_mock,
       ci_execute_tests=ci_commands_mock,
       ci_security_scan=ci_commands_mock)
    assert ci_commands_mock.mock_calls == expected_calls
