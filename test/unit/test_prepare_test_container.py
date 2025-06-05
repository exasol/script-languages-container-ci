from test.unit.test_env import test_env
from typing import Union
from unittest.mock import Mock, call

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_push_test_container import CIPushTestContainer
from exasol.slc_ci.lib.prepare_test_container import (
    prepare_test_container as lib_prepare_test_container,
)


def test_prepare_test_container(build_config_environment):
    ci_commands_mock: Union[CIPushTestContainer, CIPrepare, Mock] = Mock()

    lib_prepare_test_container(
        commit_sha=test_env.commit_sha,
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        ci_push_test_container=ci_commands_mock,
        ci_prepare=ci_commands_mock,
    )

    assert ci_commands_mock.mock_calls == [
        call.prepare(commit_sha=test_env.commit_sha),
        call.push_test_container(
            build_docker_repository=build_config_environment.docker_build_repository,
            force=True,
            commit_sha=test_env.commit_sha,
            docker_user=test_env.docker_user,
            docker_password=test_env.docker_pwd,
            test_container_folder=build_config_environment.test_container_folder,
        ),
    ]
