from test.contract_tests.test_ci_test import (
    FailingRunDBTestFlavorDBTestsContract,
    FailingRunDBTestFlavorLinkerNamespaceTestsContract,
    SuccessfulFlavorDBTestsContract,
    SuccessfulFlavorLinkerNamespaceTestsContract,
)

import pytest

from exasol_script_languages_container_ci.lib.ci_test import (
    DBTestRunner,
    DBTestRunnerProtocol,
)


class TestSuccessfulFlavorDBTestsContract(SuccessfulFlavorDBTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestSuccessfulFlavorLinkerNamespaceTestsContract(
    SuccessfulFlavorLinkerNamespaceTestsContract
):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestFailingRunDBTestFlavorDBTestsContract(FailingRunDBTestFlavorDBTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestFailingRunDBTestFlavorLinkerNamespaceTestsContract(
    FailingRunDBTestFlavorLinkerNamespaceTestsContract
):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()
