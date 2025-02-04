from test.unit import ci_calls
from test.unit.test_env import test_env
from typing import Union
from unittest.mock import MagicMock, Mock, create_autospec

import pytest

from exasol_script_languages_container_ci.lib.ci import ci
from exasol_script_languages_container_ci.lib.ci_build import CIBuild
from exasol_script_languages_container_ci.lib.ci_push import CIPush
from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest
from exasol_script_languages_container_ci.lib.config.config_data_model import Config
from exasol_script_languages_container_ci.lib.release import release
from exasol_script_languages_container_ci.lib.release_uploader import ReleaseUploader

# Testdata contain tuples of (dry_run, list(calls to CICommands))
testdata_ci = [
    (
        True,
        [
            ci_calls.prepare(),
            ci_calls.build_release_call(),
            ci_calls.run_db_test_call(),
            ci_calls.security_scan_call(),
            ci_calls.release_upload(),
        ],
    ),
    (
        False,
        [
            ci_calls.prepare(),
            ci_calls.build_release_call(),
            ci_calls.run_db_test_call(),
            ci_calls.security_scan_call(),
            ci_calls.push_release_repo(),
            ci_calls.release_upload(),
        ],
    ),
]


@pytest.mark.parametrize("is_dry_run,expected_calls", testdata_ci)
def test(is_dry_run: bool, expected_calls, build_config: Config):
    """
    Test that the correct steps are executed for the release:
     1. Build Image (force_rebuild = true/false)
     2. Run db tests
     3. Security scan
     4. Push to docker release repo (only without dry-run)
     5. Upload release to GitHub
    """
    ci_commands_mock: Union[
        CIBuild, CIPush, CIExecuteTest, CISecurityScan, ReleaseUploader, Mock
    ] = Mock()
    release(
        flavor="TEST_FLAVOR",
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        docker_release_repository=test_env.docker_release_repo,
        source_repo_url="https://github.com/test_source_repo_url",
        build_config=build_config,
        release_id=123,
        is_dry_run=is_dry_run,
        release_uploader=ci_commands_mock,  # type: ignore
        ci_build=ci_commands_mock,  # type: ignore
        ci_push=ci_commands_mock,  # type: ignore
        ci_execute_tests=ci_commands_mock,  # type: ignore
        ci_security_scan=ci_commands_mock,  # type: ignore
        ci_prepare=ci_commands_mock,  # type: ignore
    )
    assert ci_commands_mock.mock_calls == expected_calls  # type: ignore
