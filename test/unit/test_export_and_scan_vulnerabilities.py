import json
from pathlib import Path
from test.unit.test_env import test_env
from typing import Union
from unittest.mock import MagicMock, Mock, call

from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_push import CIPush
from exasol.slc_ci.lib.ci_security_scan import CISecurityScan
from exasol.slc_ci.lib.export_and_scan_vulnerabilities import (
    export_and_scan_vulnerabilities as lib_export_and_scan_vulnerabilities,
)


def test_export_and_scan_vulnerabilities_ci(build_config_environment, git_access_mock):
    res_slc_path = Path("/some_path/slc.tar.gz")
    ci_export_mock = MagicMock()
    github_output_mock = MagicMock()
    ci_export_mock.export = MagicMock(return_value=res_slc_path)
    ci_commands_mock: Union[CISecurityScan, CIPush, CIBuild, CIPrepare, Mock] = Mock()

    lib_export_and_scan_vulnerabilities(
        release=False,
        flavor=test_env.flavor_name,
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
    expected_flavor_path = str(
        build_config_environment.flavors_path / test_env.flavor_name
    )
    assert ci_commands_mock.mock_calls == [
        call.prepare(commit_sha=test_env.commit_sha),
        call.build(
            flavor_path=(expected_flavor_path,),
            rebuild=False,
            build_docker_repository=build_config_environment.docker_build_repository,
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
        "slc_release": {"goal": "release", "path": "/some_path/slc.tar.gz"},
        "slc_test": {"goal": "base_test_build_run", "path": "/some_path/slc.tar.gz"},
    }


def test_export_and_scan_vulnerabilities_cd(build_config_environment, git_access_mock):
    res_slc_path = Path("/some_path/slc.tar.gz")
    ci_export_mock = MagicMock()
    github_output_mock = MagicMock()
    ci_export_mock.export = MagicMock(return_value=res_slc_path)
    ci_commands_mock: Union[CISecurityScan, CIPush, CIBuild, CIPrepare, Mock] = Mock()

    lib_export_and_scan_vulnerabilities(
        release=True,
        flavor=test_env.flavor_name,
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
    expected_flavor_path = str(
        build_config_environment.flavors_path / test_env.flavor_name
    )
    assert ci_commands_mock.mock_calls == [
        call.prepare(commit_sha=test_env.commit_sha),
        call.build(
            flavor_path=(expected_flavor_path,),
            rebuild=True,
            build_docker_repository=build_config_environment.docker_build_repository,
            docker_user=test_env.docker_user,
            docker_password=test_env.docker_pwd,
        ),
        call.run_security_scan(flavor_path=(expected_flavor_path,)),
        call.push(
            flavor_path=(expected_flavor_path,),
            target_docker_repository=build_config_environment.docker_release_repository,
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
        "slc_release": {"goal": "release", "path": "/some_path/slc.tar.gz"},
        "slc_test": {"goal": "base_test_build_run", "path": "/some_path/slc.tar.gz"},
    }
