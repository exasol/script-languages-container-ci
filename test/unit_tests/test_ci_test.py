from contextlib import suppress
from pathlib import Path
from typing import Union
from unittest.mock import Mock, call, create_autospec, MagicMock

import pytest
from exasol_script_languages_container_tool.lib.tasks.test.test_container import AllTestsResult

from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest, DBTestRunnerProtocol
from test.mock_cast import mock_cast


class BaseCIExecuteTest:

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        self.db_test_runner_mock = create_autospec(DBTestRunnerProtocol)
        return self.db_test_runner_mock

    @pytest.fixture
    def setup_ci_execute_test(self, db_test_runner):
        self.print_file_function_mock = Mock()
        self.print_docker_images_function_mock = Mock()
        self.flavor_path = "test_flavor"
        self.test_container_folder = "test_container_folder"
        self.ci_execute_test = CIExecuteTest(
            print_file_function=self.print_file_function_mock,
            print_docker_images_function=self.print_docker_images_function_mock,
            db_test_runner=db_test_runner
        )

    @staticmethod
    def create_all_tests_result_mock(tests_are_ok: bool):
        all_tests_result: Union[MagicMock, AllTestsResult] = create_autospec(AllTestsResult)
        all_tests_result.tests_are_ok = tests_are_ok
        all_tests_result.command_line_output_path = create_autospec(Path)
        return all_tests_result

    def run_execute_tests(self):
        self.ci_execute_test.execute_tests(
            flavor_path=(self.flavor_path,),
            docker_user=None,
            docker_password=None,
            test_container_folder=self.test_container_folder,
        )

    @pytest.fixture()
    def run_db_tests_calls(self):
        return [
            call.run(flavor_path=(self.flavor_path,), test_folder=(), release_goal=('release',), workers=7,
                     docker_username=None, docker_password=None,
                     test_container_folder=self.test_container_folder),
            call.run(flavor_path=(self.flavor_path,), workers=7, test_folder=('test/linker_namespace_sanity',),
                     release_goal=('base_test_build_run',), docker_username=None, docker_password=None,
                     test_container_folder=self.test_container_folder)
        ]


class TestIntactFlavor(BaseCIExecuteTest):

    @pytest.fixture
    def setup_intact_flavor(self, setup_ci_execute_test):
        self.db_tests_all_tests_result = self.create_all_tests_result_mock(tests_are_ok=True)
        self.linker_namespace_tests_all_tests_result = self.create_all_tests_result_mock(tests_are_ok=True)
        mock_cast(self.db_test_runner_mock.run).side_effect = [self.db_tests_all_tests_result,
                                                               self.linker_namespace_tests_all_tests_result]

    @pytest.fixture
    def run_intact_flavor(self, setup_intact_flavor):
        return self.run_execute_tests()

    def test_intact_flavor_print_docker_images_function(self, run_intact_flavor):
        assert self.print_docker_images_function_mock.mock_calls == [call()]

    def test_intact_flavor_print_file_function(self, run_intact_flavor):
        assert self.print_file_function_mock.mock_calls == [
            call(self.db_tests_all_tests_result.command_line_output_path),
            call(self.linker_namespace_tests_all_tests_result.command_line_output_path)]

    def test_intact_flavor_db_test_runner_calls(self, run_intact_flavor, run_db_tests_calls):
        assert self.db_test_runner_mock.mock_calls == run_db_tests_calls


class TestBrokenTestFlavor(BaseCIExecuteTest):

    @pytest.fixture(
        params=[
            (False, True),
            (True, False),
            (False, False)
        ]
    )
    def setup_broken_test_flavor(self, setup_ci_execute_test, request):
        self.db_tests_all_tests_result = self.create_all_tests_result_mock(tests_are_ok=request.param[0])
        self.linker_namespace_tests_all_tests_result = self.create_all_tests_result_mock(tests_are_ok=request.param[1])
        mock_cast(self.db_test_runner_mock.run).side_effect = [self.db_tests_all_tests_result,
                                                               self.linker_namespace_tests_all_tests_result]

    @pytest.fixture
    def run_broken_test_flavor_suppress_execption(self, setup_broken_test_flavor):
        with suppress(Exception):
            self.run_execute_tests()

    def test_broken_test_flavor_raises(self, setup_broken_test_flavor):
        with pytest.raises(AssertionError, match="Not all tests are ok!"):
            self.run_execute_tests()

    def test_broken_test_flavor_print_docker_images_function_mock(self, run_broken_test_flavor_suppress_execption):
        assert self.print_docker_images_function_mock.mock_calls == [call()]

    def test_broken_test_flavor_print_file_function(self, run_broken_test_flavor_suppress_execption):
        assert self.print_file_function_mock.mock_calls == [
            call(self.db_tests_all_tests_result.command_line_output_path),
            call(self.linker_namespace_tests_all_tests_result.command_line_output_path)]

    def test_broken_test_flavor_db_test_runner_calls(self, run_broken_test_flavor_suppress_execption,
                                                     run_db_tests_calls):
        assert self.db_test_runner_mock.mock_calls == run_db_tests_calls
