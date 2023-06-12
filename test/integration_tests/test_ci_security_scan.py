from pathlib import Path
from unittest.mock import call, Mock

import pytest

from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from test.matchers import file_exists_matcher


def test_successful_ci_process(flavors_path, test_containers_folder):
    flavor_path = str(flavors_path / "successful_ci_process")
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    CISecurityScan(
        print_file_function=print_file_function_mock,
        print_docker_images_function=print_docker_images_function_mock
    ).run_security_scan(
        flavor_path=(flavor_path,),
    )
    assert print_file_function_mock.mock_calls == [call(file_exists_matcher())] \
           and print_docker_images_function_mock.mock_calls == [call()]


def test_broken_security_scan(flavors_path):
    flavor_path = str(flavors_path / "broken_security_scan")
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    with pytest.raises(AssertionError, match="Some security scans not successful."):
        CISecurityScan(
            print_file_function=print_file_function_mock,
            print_docker_images_function=print_docker_images_function_mock
        ).run_security_scan(
            flavor_path=(flavor_path,),
        )
    assert print_file_function_mock.mock_calls == [call(file_exists_matcher())] \
           and print_docker_images_function_mock.mock_calls == [call()]
