from pathlib import Path

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.run_tests import run_tests
from typing import Union
from unittest.mock import Mock, call

import pytest

from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest
from test.unit.v2.test_env import test_env


TEST_FLAVOR = "flavor_xyz"

@pytest.fixture
def slc_directory(tmp_path: Path) -> Path:
    with open(str(tmp_path / f'{TEST_FLAVOR}-dummy_slc.tar.gz'), 'w') as f:
        f.write("nothing")
    return tmp_path


def run_db_test_call(slc_path: Path, test_folder: str):
    return call.execute_tests(
        flavor_path=(f"flavors/{TEST_FLAVOR}",),
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        test_container_folder="test_container",
        slc_path=slc_path,
        test_folder=test_folder,
    )

def test_run_tests(slc_directory):
    ci_commands_mock: Union[CIExecuteTest,CIPrepare,Mock] = Mock()

    run_tests(
        flavor=TEST_FLAVOR,
        slc_directory=str(slc_directory),
        flavor_config=test_env.flavor_config,
        test_set_name="some_test_name",
        docker_user=test_env.docker_user,
        docker_password=test_env.docker_pwd,
        ci_prepare=ci_commands_mock,
        ci_test=ci_commands_mock
    )
    assert ci_commands_mock.mock_calls == [
        call.prepare(),
        run_db_test_call(slc_path=slc_directory / f"{TEST_FLAVOR}-dummy_slc.tar.gz", test_folder='all'),
        run_db_test_call(slc_path=slc_directory / f"{TEST_FLAVOR}-dummy_slc.tar.gz", test_folder='specific'),
    ]
