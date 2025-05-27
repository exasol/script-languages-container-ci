import datetime
import os
from pathlib import Path

from exasol_integration_test_docker_environment.lib.logging import luigi_log_config

from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_prepare import CIPrepare


def test(flavors_path, mock_settings_env_vars):
    test_type = "successful"
    flavor_path = str(flavors_path / test_type)
    CIPrepare().prepare("sha_123")
    CIBuild().build(
        flavor_path=(flavor_path,),
        rebuild=False,
        build_docker_repository="input_docker_build_repository",
        docker_user=None,
        docker_password=None,
    )
    log_path = Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME])
    assert log_path.is_file()

    OUTPUT_PATH = Path(".build_output")
    META_DATA_PATH = OUTPUT_PATH / "meta_data"
    date_path = META_DATA_PATH / "start_date"
    date = datetime.datetime.fromisoformat(date_path.read_text())
    delta = datetime.datetime.now() - date
    assert datetime.timedelta(0) <= delta < datetime.timedelta(minutes=5)
    commit_sha = META_DATA_PATH / "commit_sha"
    assert commit_sha.read_text() == "sha_123"

    security_scan_path = OUTPUT_PATH / "security_scan"

    assert security_scan_path.exists() and security_scan_path.is_dir()
