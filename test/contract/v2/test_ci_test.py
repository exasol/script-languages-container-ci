from pathlib import Path

import pytest

from exasol.slc_ci.lib.ci_export import CIExport
from exasol.slc_ci.lib.ci_test import DBTestRunnerProtocol


class CreateExistingContainer:

    @pytest.fixture
    def use_existing_container(self, tmp_path, flavor_path) -> Path:
        ci_export = CIExport()
        container_path = ci_export.export(
            flavor_path=(flavor_path,), output_directory=str(tmp_path)
        )
        return container_path


class SuccessfulFlavorContract(CreateExistingContainer):

    @pytest.fixture()
    def flavor_path(self, flavors_path):
        return str(flavors_path / "successful")

    @pytest.fixture()
    def test_container(self, test_containers_folder):
        return str(test_containers_folder / "successful")

    @pytest.fixture()
    def test_folder(self):
        return "successful_test"


class SuccessfulFlavorDBTestsContract(SuccessfulFlavorContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(
        self,
        db_test_runner: DBTestRunnerProtocol,
        test_container: str,
        flavor_path: str,
        use_existing_container: Path,
        test_folder: str,
    ):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            test_folder=(test_folder,),
            release_goal=("release",),
            workers=7,
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
            use_existing_container=str(use_existing_container),
        )
        assert result.tests_are_ok and result.command_line_output_path.exists()


class FailingRunDBTestFlavorContract(CreateExistingContainer):

    @pytest.fixture()
    def flavor_path(self, flavors_path):
        return str(flavors_path / "failing_run_db_test")

    @pytest.fixture()
    def test_container(self, test_containers_folder):
        return str(test_containers_folder / "failing")

    @pytest.fixture()
    def test_folder(self):
        return "failing_test"


class FailingRunDBTestFlavorDBTestsContract(FailingRunDBTestFlavorContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(
        self,
        db_test_runner: DBTestRunnerProtocol,
        test_container: str,
        flavor_path: str,
        use_existing_container: Path,
        test_folder: str,
    ):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            test_folder=(test_folder,),
            release_goal=("release",),
            workers=7,
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
            use_existing_container=str(use_existing_container),
        )
        assert not result.tests_are_ok and result.command_line_output_path.exists()
