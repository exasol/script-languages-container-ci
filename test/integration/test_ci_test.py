from pathlib import Path
from test.contract.test_ci_test import (
    FailingRunDBTestFlavorDBTestsContract,
    SuccessfulFlavorDBTestsContract,
)
from test.integration.utils import cleanup_images

import pytest

from exasol.slc_ci.lib.ci_test import DBTestRunner, DBTestRunnerProtocol


class TestSuccessfulFlavorDBTestsContract(SuccessfulFlavorDBTestsContract):

    @pytest.fixture(autouse=True)
    def cleanup_images(self, flavor_path):
        with cleanup_images(Path(flavor_path)):
            yield

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestFailingRunDBTestFlavorDBTestsContract(FailingRunDBTestFlavorDBTestsContract):

    @pytest.fixture(autouse=True)
    def cleanup_images(self, flavor_path):
        with cleanup_images(Path(flavor_path)):
            yield

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()
