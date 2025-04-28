import logging
from pathlib import Path

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_test import CIExecuteTest
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig


def run_tests(
    flavor: str,
    slc_directory: str,
    flavor_config: FlavorCiConfig,
    test_set_name: str,
    docker_user: str,
    docker_password: str,
    ci_prepare: CIPrepare = CIPrepare(),
    ci_test: CIExecuteTest = CIExecuteTest(),
) -> None:
    logging.info(f"Run tests for parameters: {locals()}")
    matched_test_set = [
        test_set
        for test_set in flavor_config.test_config.test_sets
        if test_set.name == test_set_name
    ]
    if len(matched_test_set) != 1:
        raise ValueError(f"Invalid test set name: {test_set_name}")
    test_set_folders = [folder for folder in matched_test_set[0].folders]
    slc_path = Path(slc_directory)
    if not slc_path.exists():
        raise ValueError(f"{slc_path} does not exist")
    slc_files = list(slc_path.glob(f"{flavor}*.tar.gz"))
    if len(slc_files) != 1:
        raise ValueError(
            f"{slc_directory} does not contain expected tar.gz file, but \n {slc_files}"
        )
    slc_file_path = slc_files[0]

    flavor_path = (f"flavors/{flavor}",)
    test_container_folder = "test_container"

    ci_prepare.prepare()
    for test_folder in test_set_folders:
        ci_test.execute_tests(
            flavor_path=flavor_path,
            slc_path=slc_file_path,
            test_folder=test_folder,
            test_container_folder=test_container_folder,
            docker_user=docker_user,
            docker_password=docker_password,
        )
