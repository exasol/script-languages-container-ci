import logging
from pathlib import Path
from typing import List

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_test import CIExecuteTest


def run_tests(
    flavor: str,
    slc_path: Path,
    test_folders: List[str],
    docker_user: str,
    docker_password: str,
    ci_prepare: CIPrepare = CIPrepare(),
    ci_test: CIExecuteTest = CIExecuteTest(),
) -> None:
    logging.info(f"Run tests for parameters: {locals()}")

    flavor_path = (f"flavors/{flavor}",)
    test_container_folder = "test_container"

    ci_prepare.prepare()
    for test_folder in test_folders:
        ci_test.execute_tests(
            flavor_path=flavor_path,
            slc_path=slc_path,
            test_folder=test_folder,
            test_container_folder=test_container_folder,
            docker_user=docker_user,
            docker_password=docker_password,
        )
