import pytest
from exasol.slc.models.accelerator import Accelerator

from exasol.slc_ci.lib.ci_export import CIExport
from exasol.slc_ci.lib.ci_test import DBTestRunnerProtocol


class SuccessfulFlavorContract:

    @pytest.fixture()
    def flavor_path(self, flavors_path):
        return str(flavors_path / "successful")

    @pytest.fixture()
    def test_container(self, test_containers_folder):
        return str(test_containers_folder / "successful")

    @pytest.fixture()
    def existing_container(self, flavor_path, tmp_path):
        export_path = tmp_path / "successful"
        export_path.mkdir(parents=True, exist_ok=False)
        ci_export = CIExport()
        slc = ci_export.export(
            flavor_path=(flavor_path,),
            goal="release",
            output_directory=str(export_path),
        )
        return slc


class SuccessfulFlavorDBTestsContract(SuccessfulFlavorContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, test_container, flavor_path, existing_container):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            test_file=(),
            test_folder=(),
            release_goal=("release",),
            generic_language_tests=tuple(),
            accelerator=Accelerator.NONE,
            workers=7,
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
            use_existing_container=existing_container,
            source_docker_tag_prefix="123",
            source_docker_repository_name="",
        )
        assert result.tests_are_ok and result.command_line_output_path.exists()


class FailingRunDBTestFlavorContract:

    @pytest.fixture()
    def flavor_path(self, flavors_path):
        return str(flavors_path / "failing_run_db_test")

    @pytest.fixture()
    def test_container(self, test_containers_folder):
        return str(test_containers_folder / "failing")

    @pytest.fixture()
    def existing_container(self, flavor_path, tmp_path):
        export_path = tmp_path / "failure"
        export_path.mkdir(parents=True, exist_ok=False)
        ci_export = CIExport()
        slc = ci_export.export(
            flavor_path=(flavor_path,),
            goal="release",
            output_directory=str(export_path),
        )
        return slc


class FailingRunDBTestFlavorDBTestsContract(FailingRunDBTestFlavorContract):

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, test_container, flavor_path, existing_container):
        result = db_test_runner.run(
            flavor_path=(flavor_path,),
            test_file=(),
            test_folder=(),
            release_goal=("release",),
            generic_language_tests=tuple(),
            accelerator=Accelerator.NONE,
            workers=7,
            docker_username=None,
            docker_password=None,
            test_container_folder=test_container,
            use_existing_container=existing_container,
            source_docker_tag_prefix="123",
            source_docker_repository_name="",
        )
        assert not result.tests_are_ok and result.command_line_output_path.exists()
