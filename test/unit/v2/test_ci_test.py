from contextlib import suppress
from pathlib import Path
from test.mock_cast import mock_cast
from typing import Union
from unittest.mock import MagicMock, call, create_autospec

import pytest
from exasol.slc.models.test_result import AllTestsResult

from exasol.slc_ci.lib.ci_step_output_printer import CIStepOutputPrinterProtocol
from exasol.slc_ci.lib.ci_test import CIExecuteTest, DBTestRunnerProtocol


class BaseCIExecuteTest:

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        self.db_test_runner_mock = create_autospec(DBTestRunnerProtocol)
        return self.db_test_runner_mock

    @pytest.fixture
    def base_setup(self, db_test_runner):
        self.printer_mock = create_autospec(CIStepOutputPrinterProtocol)
        self.flavor_path = "test_flavor"
        self.test_container_folder = "test_container_folder"
        self.slc_path = Path.cwd()
        self.test_folder = "test_folder"
        self.ci_execute_test = CIExecuteTest(
            printer=self.printer_mock, db_test_runner=db_test_runner
        )

    @staticmethod
    def create_all_tests_result_mock(tests_are_ok: bool):
        all_tests_result: Union[MagicMock, AllTestsResult] = create_autospec(
            AllTestsResult
        )
        all_tests_result.tests_are_ok = tests_are_ok
        all_tests_result.command_line_output_path = create_autospec(Path)
        return all_tests_result

    def execute_tests(self):
        self.ci_execute_test.execute_tests(
            flavor_path=(self.flavor_path,),
            docker_user=None,
            docker_password=None,
            test_container_folder=self.test_container_folder,
            slc_path=self.slc_path,
            test_folder=self.test_folder,
        )

    @pytest.fixture()
    def run_db_tests_calls(self):
        return [
            call.run(
                flavor_path=(self.flavor_path,),
                test_folder=(self.test_folder,),
                release_goal=("release",),
                workers=7,
                docker_username=None,
                docker_password=None,
                test_container_folder=self.test_container_folder,
                use_existing_container=str(self.slc_path),
            ),
        ]


class TestSuccessfulFlavor(BaseCIExecuteTest):

    @pytest.fixture
    def complete_setup(self, base_setup):
        self.db_tests_all_tests_result = self.create_all_tests_result_mock(
            tests_are_ok=True
        )
        mock_cast(self.db_test_runner_mock.run).side_effect = [
            self.db_tests_all_tests_result,
        ]

    def test_ci_step_output_printer_call(self, complete_setup):
        self.execute_tests()
        assert self.printer_mock.mock_calls == [
            call.print_file(self.db_tests_all_tests_result.command_line_output_path),
            call.print_exasol_docker_images(),
        ]

    def test_db_test_runner_calls(self, complete_setup, run_db_tests_calls):
        self.execute_tests()
        assert self.db_test_runner_mock.mock_calls == run_db_tests_calls


class TestFailingRunDBTestFlavor(BaseCIExecuteTest):

    @pytest.fixture()
    def complete_setup(self, base_setup):
        self.db_tests_all_tests_result = self.create_all_tests_result_mock(
            tests_are_ok=False
        )
        mock_cast(self.db_test_runner_mock.run).side_effect = [
            self.db_tests_all_tests_result,
        ]

    @pytest.fixture
    def run_suppress_exception(self, complete_setup):
        with suppress(Exception):
            self.execute_tests()

    def test_raises(self, complete_setup):
        with pytest.raises(AssertionError, match="Not all tests are ok!"):
            self.execute_tests()

    def test_ci_step_output_printer_call(self, run_suppress_exception):
        assert self.printer_mock.mock_calls == [
            call.print_file(self.db_tests_all_tests_result.command_line_output_path),
            call.print_exasol_docker_images(),
        ]

    def test_db_test_runner_calls(self, run_suppress_exception, run_db_tests_calls):
        assert self.db_test_runner_mock.mock_calls == run_db_tests_calls
