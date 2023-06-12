import pytest

from exasol_script_languages_container_ci.lib.ci_test import DBTestRunner, DBTestRunnerProtocol
from test.contract_tests.test_ci_test import IntactFlavorDBTestsContract, IntactFlavorLinkerNamespaceTestsContract, \
    BrokenTestFlavorDBTestsContract, BrokenTestFlavorLinkerNamespaceTestsContract


@pytest.fixture()
def intact_flavor_path(flavors_path):
    return str(flavors_path / "successful_ci_process")


@pytest.fixture()
def broken_test_flavor_path(flavors_path):
    return str(flavors_path / "broken_run_db_test")


@pytest.fixture()
def successful_test_test_container(test_containers_folder):
    return str(test_containers_folder / "successful_test")


@pytest.fixture()
def broken_test_test_container(test_containers_folder):
    return str(test_containers_folder / "broken_test")


class TestIntactFlavorDBTestsContract(IntactFlavorDBTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestIntactFlavorLinkerNamespaceTestsContract(IntactFlavorLinkerNamespaceTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestBrokenTestFlavorDBTestsContract(BrokenTestFlavorDBTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()


class TestBrokenTestFlavorLinkerNamespaceTestsContract(BrokenTestFlavorLinkerNamespaceTestsContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        return DBTestRunner()
