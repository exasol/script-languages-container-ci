import logging
from pathlib import Path
from typing import Tuple, Callable, Protocol, Optional

from exasol_integration_test_docker_environment.cli.options.test_environment_options import LATEST_DB_VERSION
from exasol_script_languages_container_tool.lib.api.run_db_tests import run_db_test

from exasol_script_languages_container_ci.lib.common import print_docker_images, print_file

from exasol_script_languages_container_tool.lib.tasks.test.test_container import AllTestsResult


def _print_docker_images_function():
    print_docker_images(logging.info)


def _print_file_function(path: Path):
    print_file(path, logging.info)


class RunDBTestsProtocol(Protocol):
    def __call__(self,
                 flavor_path: Tuple[str, ...],
                 release_goal: Tuple[str, ...],
                 test_folder: Tuple[str, ...],
                 test_container_folder: str,
                 workers: int,
                 source_docker_username: str,
                 source_docker_password: str) -> AllTestsResult:
        ...


class CIExecuteTest:

    def __init__(self,
                 print_file_function: Callable[[Path], None] = _print_file_function,
                 print_docker_images_function: Callable[[], None] = _print_docker_images_function,
                 run_db_test: RunDBTestsProtocol = run_db_test):
        self._run_db_test = run_db_test
        self._print_docker_images_function = print_docker_images_function
        self._print_file_function = print_file_function

    def execute_tests(self,
                      flavor_path: Tuple[str, ...],
                      docker_user: str,
                      docker_password: str,
                      test_container_folder: str):
        """
        Run db tests
        """
        db_tests_are_ok = self.run_db_tests(flavor_path=flavor_path,
                                            docker_user=docker_user,
                                            docker_password=docker_password,
                                            test_container_folder=test_container_folder)
        linker_namespace_tests_are_ok = self.run_linker_namespace_tests(flavor_path=flavor_path,
                                                                        docker_user=docker_user,
                                                                        docker_password=docker_password,
                                                                        test_container_folder=test_container_folder)
        self._print_docker_images_function()
        tests_are_ok = db_tests_are_ok and linker_namespace_tests_are_ok
        if not tests_are_ok:
            raise AssertionError("Not all tests are ok!")

    def run_db_tests(self, flavor_path: Tuple[str, ...],
                     docker_user: str,
                     docker_password: str,
                     test_container_folder: str) -> bool:
        logging.info(f"Running command 'run_db_test' for flavor-path {flavor_path}")
        db_test_result = \
            self._run_db_test(flavor_path=flavor_path,
                              test_folder=tuple(),
                              release_goal=('release',),
                              workers=7,
                              source_docker_username=docker_user,
                              source_docker_password=docker_password,
                              test_container_folder=test_container_folder)
        self._print_file_function(db_test_result.command_line_output_path)
        return db_test_result.tests_are_ok

    def run_linker_namespace_tests(self,
                                   flavor_path: Tuple[str, ...],
                                   docker_user: str,
                                   docker_password: str,
                                   test_container_folder: str) -> bool:
        logging.info(f"Running command 'run_db_test' for linker_namespace_sanity for flavor-path {flavor_path}")
        linker_namespace_test_result = \
            self._run_db_test(flavor_path=flavor_path, workers=7,
                              test_folder=("test/linker_namespace_sanity",),
                              release_goal=("base_test_build_run",),
                              source_docker_username=docker_user,
                              source_docker_password=docker_password,
                              test_container_folder=test_container_folder)
        self._print_file_function(linker_namespace_test_result.command_line_output_path)
        return linker_namespace_test_result.tests_are_ok
