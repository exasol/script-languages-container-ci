import os
from pathlib import Path
from test.unit.github.test_env import test_env
from typing import Tuple, Union
from unittest.mock import Mock, call

import pytest
from exasol.slc.models.accelerator import Accelerator

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_test import CIExecuteTest
from exasol.slc_ci.lib.run_tests import run_tests


@pytest.fixture
def slc_directory(tmp_path: Path) -> Path:
    with open(str(tmp_path / f"{test_env.flavor_name}-dummy_slc.tar.gz"), "w") as f:
        f.write("nothing")
    return tmp_path


def run_db_test_call(
    slc_path: Path,
    goal: str,
    test_folder: str,
    test_container_folder: str,
    flavor_path: str,
    generic_language_tests: Tuple[str, ...],
    accelerator: Accelerator,
    build_docker_repository: str,
):
    return call.execute_tests(
        flavor_path=(flavor_path,),
        slc_path=slc_path,
        test_folder=test_folder,
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        test_container_folder=test_container_folder,
        goal=goal,
        generic_language_tests=generic_language_tests,
        accelerator=accelerator,
        commit_sha=test_env.commit_sha,
        build_docker_repository=build_docker_repository,
    )


TEST_DATA = [t.dict().values() for t in test_env.flavor_ci_config.test_config.test_sets]


@pytest.mark.parametrize(
    "name, folders, goal, generic_language_tests, test_runner, accelerator", TEST_DATA
)
def test_run_tests(
    slc_directory,
    build_config_with_flavor_environment,
    name,
    folders,
    goal,
    generic_language_tests,
    test_runner,
    accelerator,
):
    ci_commands_mock: Union[CIExecuteTest, CIPrepare, Mock] = Mock()

    c = os.getcwd()
    run_tests(
        flavor=test_env.flavor_name,
        slc_directory=str(slc_directory),
        test_set_name=name,
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        ci_prepare=ci_commands_mock,
        ci_test=ci_commands_mock,
        commit_sha=test_env.commit_sha,
    )
    assert ci_commands_mock.mock_calls == [
        call.prepare(),
        run_db_test_call(
            slc_path=slc_directory / f"{test_env.flavor_name}-dummy_slc.tar.gz",
            goal=goal,
            test_folder=folders[0] if folders else "",
            test_container_folder=build_config_with_flavor_environment.test_container_folder,
            flavor_path=str(
                build_config_with_flavor_environment.flavors_path / test_env.flavor_name
            ),
            generic_language_tests=tuple(generic_language_tests),
            accelerator=accelerator,
            build_docker_repository=build_config_with_flavor_environment.docker_build_repository,
        ),
    ]
