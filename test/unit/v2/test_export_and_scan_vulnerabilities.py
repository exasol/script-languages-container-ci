from pathlib import Path

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.export_and_scan_vulnerabilities import export_and_scan_vulnerabilities
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig, TestConfig, TestSet
from typing import Union
from unittest.mock import Mock, call, MagicMock

import pytest

from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest
from test.unit.v2.test_env import test_env

TEST_FLAVOR = "flavor_xyz"

FLAVOR_CONFIG = FlavorCiConfig(
    build_runner="some_build_runner",
    test_config=TestConfig(
        test_runner="some_test_runner",
        test_sets=[TestSet(name="some_test_name", folders=["all", "specific"])],
    ),
)

@pytest.fixture
def slc_directory(tmp_path: Path) -> Path:
    with open(str(tmp_path / f'{TEST_FLAVOR}-dummy_slc.tar.gz'), 'w') as f:
        f.write("nothing")
    return tmp_path



def test_export_and_scan_vulnerabilities(slc_directory, git_access_mock):
    res_slc_path = Path("/some_path/slc.tar.gz")
    ci_export_mock = MagicMock()
    ci_export_mock.export = MagicMock(return_value=res_slc_path)
    ci_commands_mock: Union[CIExecuteTest,CIPrepare,Mock] = Mock()

    result = export_and_scan_vulnerabilities(
        flavor=TEST_FLAVOR,
        branch_name=test_env.branch_name,
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        commit_sha=test_env.commit_sha,
        build_config=test_env.build_config,
        git_access=git_access_mock,
        ci_build=ci_commands_mock,
        ci_security_scan=ci_commands_mock,
        ci_prepare=ci_commands_mock,
        ci_export=ci_export_mock,
        ci_push=ci_commands_mock,
    )
    expected_flavor_path = str(test_env.build_config.flavors_path / TEST_FLAVOR)
    assert ci_commands_mock.mock_calls == [
        call.prepare(),
        call.build(flavor_path=(expected_flavor_path,), rebuild=False,
                   build_docker_repository=test_env.build_config.docker_build_repository, commit_sha=test_env.commit_sha,
                   docker_user=test_env.docker_user, docker_password=test_env.docker_pwd,
                   test_container_folder=test_env.build_config.test_container_folder,),
        call.run_security_scan(flavor_path=(expected_flavor_path,)),
        call.push(flavor_path=(expected_flavor_path,), target_docker_repository=test_env.build_config.docker_build_repository,
                  target_docker_tag_prefix=test_env.commit_sha, docker_user=test_env.docker_user,
                  docker_password=test_env.docker_pwd),
        call.push(flavor_path=(expected_flavor_path,), target_docker_repository=test_env.build_config.docker_build_repository,
                  target_docker_tag_prefix='', docker_user=test_env.docker_user, docker_password=test_env.docker_pwd),
    ]
    assert ci_export_mock.mock_calls == [call.export(flavor_path=(expected_flavor_path,))]
    assert result == res_slc_path
