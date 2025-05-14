from test.contract.test_ci_test import (
    FailingRunDBTestFlavorDBTestsContract,
    SuccessfulFlavorDBTestsContract,
)

import pytest

from exasol.slc_ci.lib.ci_test import DBTestRunner, DBTestRunnerProtocol


class TestSuccessfulFlavorDBTestsContract(SuccessfulFlavorDBTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestFailingRunDBTestFlavorDBTestsContract(FailingRunDBTestFlavorDBTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()