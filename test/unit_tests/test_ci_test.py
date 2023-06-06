from pathlib import Path
from typing import Union
from unittest.mock import Mock, call, create_autospec, MagicMock

import pytest

from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest
from test.matchers import regex_matcher
from exasol_script_languages_container_tool.lib.tasks.test.test_container import AllTestsResult, FlavorTestResult

from test.mock_cast import mock_cast

TEST_CONTAINER = "test_container"

FLAVOR = "test_flavor"


def test_functioning():
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    run_db_test_mock = Mock()
    db_tests_all_tests_result = create_all_tests_result_mock(tests_are_ok=True)
    linker_namespace_all_tests_result = create_all_tests_result_mock(tests_are_ok=True)
    run_db_test_mock.side_effect = [db_tests_all_tests_result, linker_namespace_all_tests_result]
    CIExecuteTest(
        print_file_function=print_file_function_mock,
        print_docker_images_function=print_docker_images_function_mock,
        run_db_test=run_db_test_mock
    ).execute_tests(
        flavor_path=(FLAVOR,),
        docker_user=None,
        docker_password=None,
        test_container_folder=TEST_CONTAINER,

    )
    assert print_file_function_mock.mock_calls == [
        call(db_tests_all_tests_result.command_line_output_path),
        call(linker_namespace_all_tests_result.command_line_output_path)] \
           and print_docker_images_function_mock.mock_calls == [call()] \
           and run_db_test_mock.mock_calls == [
               call(flavor_path=(FLAVOR,), test_folder=(), release_goal=('release',), workers=7,
                    source_docker_username=None, source_docker_password=None, test_container_folder=TEST_CONTAINER),
               call(flavor_path=(FLAVOR,), workers=7, test_folder=('test/linker_namespace_sanity',),
                    release_goal=('base_test_build_run',), source_docker_username=None, source_docker_password=None,
                    test_container_folder=TEST_CONTAINER)
           ]


# TODO parameterize
def test_broken_db_test():
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    run_db_test_mock = Mock()
    db_tests_all_tests_result = create_all_tests_result_mock(tests_are_ok=False)
    linker_namespace_all_tests_result = create_all_tests_result_mock(tests_are_ok=False)
    run_db_test_mock.side_effect = [db_tests_all_tests_result, linker_namespace_all_tests_result]
    with pytest.raises(AssertionError, match="Not all tests are ok!"):
        CIExecuteTest(
            print_file_function=print_file_function_mock,
            print_docker_images_function=print_docker_images_function_mock,
            run_db_test=run_db_test_mock
        ).execute_tests(
            flavor_path=(FLAVOR,),
            docker_user=None,
            docker_password=None,
            test_container_folder=TEST_CONTAINER,
        )
    assert print_file_function_mock.mock_calls == [
        call(db_tests_all_tests_result.command_line_output_path),
        call(linker_namespace_all_tests_result.command_line_output_path)] \
           and print_docker_images_function_mock.mock_calls == [call()] \
           and run_db_test_mock.mock_calls == [
               call(flavor_path=(FLAVOR,), test_folder=(), release_goal=('release',), workers=7,
                    source_docker_username=None, source_docker_password=None, test_container_folder=TEST_CONTAINER),
               call(flavor_path=(FLAVOR,), workers=7, test_folder=('test/linker_namespace_sanity',),
                    release_goal=('base_test_build_run',), source_docker_username=None, source_docker_password=None,
                    test_container_folder=TEST_CONTAINER)
           ]


def create_all_tests_result_mock(tests_are_ok: bool):
    all_tests_result: Union[MagicMock, AllTestsResult] = create_autospec(AllTestsResult)
    all_tests_result.tests_are_ok = tests_are_ok
    all_tests_result.command_line_output_path = Mock()
    return all_tests_result
