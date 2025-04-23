from pathlib import Path
from typing import List

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_test import CIExecuteTest
from exasol.slc_ci.lib.run_tests import run_tests as lib_run_tests


def run_tests(
    flavor: str,
    slc_path: Path,
    test_folders: List[str],
    docker_user: str,
    docker_password: str,
) -> None:
    ci_test = CIExecuteTest()
    ci_prepare = CIPrepare()

    return lib_run_tests(
        flavor=flavor,
        slc_path=slc_path,
        test_folders=test_folders,
        docker_user=docker_user,
        docker_password=docker_password,
        ci_prepare=ci_prepare,
        ci_test=ci_test,
    )
