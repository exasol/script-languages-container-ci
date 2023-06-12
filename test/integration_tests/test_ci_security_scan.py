from pathlib import Path
from unittest.mock import call, Mock, create_autospec

import pytest

from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from exasol_script_languages_container_ci.lib.ci_step_output_printer import CIStepOutputPrinterProtocol
from test.matchers import file_exists_matcher


def test_successful_ci_process(flavors_path, test_containers_folder):
    flavor_path = str(flavors_path / "successful_ci_process")
    ci_step_output_printer_mock = create_autospec(CIStepOutputPrinterProtocol)
    CISecurityScan(
        ci_step_output_printer=ci_step_output_printer_mock
    ).run_security_scan(
        flavor_path=(flavor_path,),
    )
    assert ci_step_output_printer_mock.mock_calls == [
        call.print_file(file_exists_matcher()),
        call.print_docker_images()]


def test_broken_security_scan(flavors_path):
    flavor_path = str(flavors_path / "broken_security_scan")
    ci_step_output_printer_mock = create_autospec(CIStepOutputPrinterProtocol)
    with pytest.raises(AssertionError, match="Some security scans not successful."):
        CISecurityScan(
            ci_step_output_printer=ci_step_output_printer_mock
        ).run_security_scan(
            flavor_path=(flavor_path,),
        )
    assert ci_step_output_printer_mock.mock_calls == [
        call.print_file(file_exists_matcher()),
        call.print_docker_images()]
