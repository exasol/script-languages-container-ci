import json
from pathlib import Path
from test.unit.github.test_env import test_env
from typing import Union
from unittest.mock import MagicMock, Mock, call

from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_push import CIPush
from exasol.slc_ci.lib.ci_security_scan import CISecurityScan
from exasol.slc_ci.lib.export_and_scan_vulnerabilities import (
    export_and_scan_vulnerabilities as lib_export_and_scan_vulnerabilities,
)

TEST_FLAVOR = "flavor_xyz"


def test_export_and_scan_vulnerabilities(build_config_environment, git_access_mock):
    res_slc_path = Path("/some_path/slc.tar.gz")
    ci_export_mock = MagicMock()
    github_output_mock = MagicMock()
    ci_export_mock.export = MagicMock(return_value=res_slc_path)
    ci_commands_mock: Union[CISecurityScan, CIPush, CIBuild, CIPrepare, Mock] = Mock()

    lib_export_and_scan_vulnerabilities(
        flavor=TEST_FLAVOR,
        branch_name=test_env.branch_name,
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        commit_sha=test_env.commit_sha,
        git_access=git_access_mock,
        github_access=github_output_mock,
        ci_build=ci_commands_mock,
        ci_security_scan=ci_commands_mock,
        ci_prepare=ci_commands_mock,
        ci_export=ci_export_mock,
        ci_push=ci_commands_mock,
    )
    expected_flavor_path = str(build_config_environment.flavors_path / TEST_FLAVOR)
    assert ci_commands_mock.mock_calls == [
        call.prepare(),
        call.build(
            flavor_path=(expected_flavor_path,),
            rebuild=False,
            build_docker_repository=build_config_environment.docker_build_repository,
            commit_sha=test_env.commit_sha,
            docker_user=test_env.docker_user,
            docker_password=test_env.docker_pwd,
        ),
        call.run_security_scan(flavor_path=(expected_flavor_path,)),
        call.push(
            flavor_path=(expected_flavor_path,),
            target_docker_repository=build_config_environment.docker_build_repository,
            target_docker_tag_prefix=test_env.commit_sha,
            docker_user=test_env.docker_user,
            docker_password=test_env.docker_pwd,
        ),
        call.push(
            flavor_path=(expected_flavor_path,),
            target_docker_repository=build_config_environment.docker_build_repository,
            target_docker_tag_prefix="",
            docker_user=test_env.docker_user,
            docker_password=test_env.docker_pwd,
        ),
    ]
    assert ci_export_mock.mock_calls == [
        call.export(
            flavor_path=(expected_flavor_path,),
            goal="release",
            output_directory=".build_output_release",
        ),
        call.export(
            flavor_path=(expected_flavor_path,),
            goal="base_test_build_run",
            output_directory=".build_output_test",
        ),
    ]
    assert json.loads(github_output_mock.write_result.call_args.args[0]) == {
        "slc_release": "/some_path/slc.tar.gz",
        "slc_test": "/some_path/slc.tar.gz",
    }
