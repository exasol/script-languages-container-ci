import logging
from pathlib import Path
from typing import Tuple, Callable

from exasol_script_languages_container_tool.lib.api import security_scan

from exasol_script_languages_container_ci.lib.ci_step_output_printer import CIStepOutputPrinterProtocol, \
    CIStepOutputPrinter
from exasol_script_languages_container_ci.lib.common import print_file, print_docker_images


def _print_docker_images_function():
    print_docker_images(logging.info)


def _print_file_function(path: Path):
    print_file(path, logging.info)


class CISecurityScan:

    def __init__(self, ci_step_output_printer: CIStepOutputPrinterProtocol = CIStepOutputPrinter(logging.info)):
        self._ci_step_output_printer = ci_step_output_printer

    def run_security_scan(self,
                          flavor_path: Tuple[str, ...]):
        """
        Run security scan and print result
        """

        logging.info(f"Running command 'security_scan' with parameters {locals()}")
        security_scan_result = security_scan(flavor_path=flavor_path, workers=7)
        logging.info("============= SECURITY REPORT ===========")
        self._ci_step_output_printer.print_file(Path(security_scan_result.report_path))
        self._ci_step_output_printer.print_docker_images()
        if not security_scan_result.scans_are_ok:
            raise AssertionError("Some security scans not successful.")
