from pathlib import Path
from unittest.mock import Mock, call

import pytest

from exasol_script_languages_container_ci.lib.ci_test import CIExecuteTest
from test.matchers import regex_matcher, file_exists_matcher


def test_functioning(flavors_path: Path, test_container_folder: Path):
    flavor_path = str(flavors_path / "functioning")
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    CIExecuteTest(
        print_file_function=print_file_function_mock,
        print_docker_images_function=print_docker_images_function_mock
    ).execute_tests(
        flavor_path=(flavor_path,),
        docker_user=None,
        docker_password=None,
        test_container_folder=str(test_container_folder),

    )
    assert print_file_function_mock.mock_calls == \
           [call(file_exists_matcher()),
            call(file_exists_matcher())] \
           and print_docker_images_function_mock.mock_calls == [call()]


def test_broken_test(flavors_path: Path, test_container_folder: Path):
    flavor_path = str(flavors_path / "broken-test")
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    with pytest.raises(Exception):
        CIExecuteTest(
            print_file_function=print_file_function_mock,
            print_docker_images_function=print_docker_images_function_mock
        ).execute_tests(
            flavor_path=(flavor_path,),
            docker_user=None,
            docker_password=None,
            test_container_folder=str(test_container_folder),
        )
        assert print_file_function_mock.mock_calls == [
            call(file_exists_matcher()),
            call(file_exists_matcher())] \
               and print_docker_images_function_mock.mock_calls == [call()]
