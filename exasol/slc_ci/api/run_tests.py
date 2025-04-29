from pathlib import Path

from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_test import CIExecuteTest
from exasol.slc_ci.lib.run_tests import run_tests as lib_run_tests
from exasol.slc_ci.model.build_config import BuildConfig
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig


def run_tests(
    flavor: str,
    slc_directory: str,
    flavor_config: FlavorCiConfig,
    build_config: BuildConfig,
    test_set_name: str,
    docker_user: str,
    docker_password: str,
) -> None:
    ci_test = CIExecuteTest()
    ci_prepare = CIPrepare()

    return lib_run_tests(
        flavor=flavor,
        slc_directory=slc_directory,
        flavor_config=flavor_config,
        build_config=build_config,
        test_set_name=test_set_name,
        docker_user=docker_user,
        docker_password=docker_password,
        ci_prepare=ci_prepare,
        ci_test=ci_test,
    )
