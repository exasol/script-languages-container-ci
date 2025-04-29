import os
from pathlib import Path


from exasol_integration_test_docker_environment.lib.logging import luigi_log_config

from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_prepare import CIPrepare


def test(flavors_path, test_containers_folder, mock_settings_env_vars):
    test_type = "successful"
    flavor_path = str(flavors_path / test_type)
    test_container_folder = str(test_containers_folder / test_type)
    CIPrepare().prepare()
    CIBuild().build(
        flavor_path=(flavor_path,),
        rebuild=False,
        commit_sha="COMMIT_SHA",
        build_docker_repository="input_docker_build_repository",
        docker_user=None,
        docker_password=None,
        test_container_folder=test_container_folder,
    )
    log_path = Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME])
    assert log_path.is_file()
