from unittest.mock import call, create_autospec

import pytest

from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from exasol_script_languages_container_ci.lib.ci_step_output_printer import CIStepOutputPrinterProtocol
from test.matchers import file_exists_matcher


def test_successful_flavor(flavors_path, test_containers_folder):
    flavor_path = str(flavors_path / "successful")
    printer_mock = create_autospec(CIStepOutputPrinterProtocol)
    CISecurityScan(
        printer=printer_mock
    ).run_security_scan(
        flavor_path=(flavor_path,),
    )
    assert printer_mock.mock_calls == [
        call.print_file(file_exists_matcher()),
        call.print_docker_images()]


def test_failing_security_scan(flavors_path):
    flavor_path = str(flavors_path / "failing_security_scan")
    printer_mock = create_autospec(CIStepOutputPrinterProtocol)
    with pytest.raises(AssertionError, match="Some security scans not successful."):
        CISecurityScan(
            printer=printer_mock
        ).run_security_scan(
            flavor_path=(flavor_path,),
        )
    assert printer_mock.mock_calls == [
        call.print_file(file_exists_matcher()),
        call.print_docker_images()]
