import pytest
from exasol_integration_test_docker_environment.lib.api.api_errors import (
    TaskRuntimeError,
)

from exasol_script_languages_container_ci.lib.ci_test import DBTestRunnerProtocol


class SuccessfulFlavorContract:

    @pytest.fixture()
    def flavor_path(self, flavors_path):
        return str(flavors_path / "successful")

    @pytest.fixture()
    def test_container(self, test_containers_folder):
        return str(test_containers_folder / "successful")


class SuccessfulFlavorDBTestsContract(SuccessfulFlavorContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, test_container, flavor_path):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            test_folder=(),
            release_goal=("release",),
            workers=7,
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
        )
        assert result.tests_are_ok and result.command_line_output_path.exists()


class SuccessfulFlavorLinkerNamespaceTestsContract(SuccessfulFlavorContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, test_container, flavor_path):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            workers=7,
            test_folder=("test/linker_namespace_sanity",),
            release_goal=("base_test_build_run",),
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
        )
        assert result.tests_are_ok and result.command_line_output_path.exists()


class FailingRunDBTestFlavorContract:

    @pytest.fixture()
    def flavor_path(self, flavors_path):
        return str(flavors_path / "failing_run_db_test")

    @pytest.fixture()
    def test_container(self, test_containers_folder):
        return str(test_containers_folder / "failing")


class FailingRunDBTestFlavorDBTestsContract(FailingRunDBTestFlavorContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, test_container, flavor_path):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            test_folder=(),
            release_goal=("release",),
            workers=7,
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
        )
        assert not result.tests_are_ok and result.command_line_output_path.exists()


class FailingRunDBTestFlavorLinkerNamespaceTestsContract(
    FailingRunDBTestFlavorContract
):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, test_container, flavor_path):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            workers=7,
            test_folder=("linker_namespace_sanity",),
            release_goal=("base_test_build_run",),
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
        )
        assert not result.tests_are_ok and result.command_line_output_path.exists()
