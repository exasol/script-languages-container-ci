import pytest
from exasol_integration_test_docker_environment.lib.api.api_errors import TaskRuntimeError

from exasol_script_languages_container_ci.lib.ci_test import DBTestRunnerProtocol


@pytest.fixture()
def intact_flavor_path(flavors_path):
    return str(flavors_path / "intact")


@pytest.fixture()
def broken_test_flavor_path(flavors_path):
    return str(flavors_path / "broken-test")


class IntactFlavorDBTestsContract:

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, successful_test_test_container, intact_flavor_path):
        try:
            result = db_test_runner.run(flavor_path=(intact_flavor_path,), test_folder=(),
                                        release_goal=('release',), workers=7,
                                        docker_username=None, docker_password=None,
                                        test_container_folder=successful_test_test_container)
            assert result.tests_are_ok and result.command_line_output_path.exists()
        except TaskRuntimeError as e:
            for i in e.inner:
                print(i)
            raise e


class IntactFlavorLinkerNamespaceTestsContract:

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, successful_test_test_container, intact_flavor_path):
        try:
            result = db_test_runner.run(flavor_path=(intact_flavor_path,), workers=7,
                                        test_folder=('test/linker_namespace_sanity',),
                                        release_goal=('base_test_build_run',),
                                        docker_username=None, docker_password=None,
                                        test_container_folder=successful_test_test_container)
            assert result.tests_are_ok and result.command_line_output_path.exists()
        except TaskRuntimeError as e:
            for i in e.inner:
                print(i)
            raise e


class BrokenTestFlavorDBTestsContract:

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, broken_test_test_container, broken_test_flavor_path):
        result = db_test_runner.run(flavor_path=(broken_test_flavor_path,), test_folder=(),
                                    release_goal=('release',), workers=7,
                                    docker_username=None, docker_password=None,
                                    test_container_folder=broken_test_test_container)
        assert not result.tests_are_ok and result.command_line_output_path.exists()


class BrokenTestFlavorLinkerNamespaceTestsContract:

    @pytest.fixture
    def db_test_runner(self) -> DBTestRunnerProtocol:
        raise NotImplementedError()

    def test(self, db_test_runner, broken_test_test_container, broken_test_flavor_path):
        result = db_test_runner.run(flavor_path=(broken_test_flavor_path,), workers=7,
                                    test_folder=('linker_namespace_sanity',),
                                    release_goal=('base_test_build_run',),
                                    docker_username=None, docker_password=None,
                                    test_container_folder=broken_test_test_container)
        assert not result.tests_are_ok and result.command_line_output_path.exists()
