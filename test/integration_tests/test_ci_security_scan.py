from pathlib import Path
from unittest.mock import call, Mock

import pytest

from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from test.matchers import file_exists_matcher


def test_functioning():
    script_path = Path(__file__).absolute().parent
    resources_path = script_path / "resources"
    flavor_path = str(resources_path / "flavors" / "functioning")
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    security_scan_result = \
        CISecurityScan(
            print_file_function=print_file_function_mock,
            print_docker_images_function=print_docker_images_function_mock
        ).run_security_scan(
            flavor_path=(flavor_path,),
        )
    assert print_file_function_mock.mock_calls == [call(file_exists_matcher())] \
           and print_docker_images_function_mock.mock_calls == [call()]


def test_broken_security_scan():
    script_path = Path(__file__).absolute().parent
    resources_path = script_path / "resources"
    flavor_path = str(resources_path / "flavors" / "broken-security-scan")
    print_file_function_mock = Mock()
    print_docker_images_function_mock = Mock()
    with pytest.raises(AssertionError, match="Some security scans not successful."):
        security_scan_result = \
            CISecurityScan(
                print_file_function=print_file_function_mock,
                print_docker_images_function=print_docker_images_function_mock
            ).run_security_scan(
                flavor_path=(flavor_path,),
            )
    assert print_file_function_mock.mock_calls == [call(file_exists_matcher())] \
           and print_docker_images_function_mock.mock_calls == [call()]
