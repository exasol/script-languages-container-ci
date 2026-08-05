import datetime
import os
from pathlib import Path
from test.integration.utils import cleanup_images

from exasol_integration_test_docker_environment.cli.options.system_options import (
    DEFAULT_OUTPUT_DIRECTORY,
)
from exasol_integration_test_docker_environment.lib.logging import luigi_log_config

from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_prepare import CIPrepare


def test(flavors_path, mock_settings_env_vars, tmp_test_dir):
    test_type = "successful"
    build_name = "test-1.2.3"
    flavor_path = str(flavors_path / test_type)
    with cleanup_images(Path(flavor_path)):
        CIPrepare().prepare("sha_123")
        CIBuild().build(
            flavor_path=(flavor_path,),
            rebuild=False,
            build_docker_repository="input_docker_build_repository",
            docker_user=None,
            docker_password=None,
            build_name=build_name,
        )
        log_path = Path(os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME])
        assert log_path.is_file()

        output_path = Path(DEFAULT_OUTPUT_DIRECTORY)
        meta_data_path = output_path / "meta_data"
        date_path = meta_data_path / "start_date"
        date = datetime.datetime.fromisoformat(date_path.read_text())
        delta = datetime.datetime.now() - date
        assert datetime.timedelta(0) <= delta < datetime.timedelta(minutes=5)
        commit_sha = meta_data_path / "commit_sha"
        assert commit_sha.read_text() == "sha_123"

        security_scan_path = output_path / "security_scan"

        assert security_scan_path.exists() and security_scan_path.is_dir()
