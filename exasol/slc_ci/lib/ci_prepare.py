import os
from datetime import datetime
from pathlib import Path

from exasol_integration_test_docker_environment.cli.options.system_options import (
    DEFAULT_OUTPUT_DIRECTORY,
)
from exasol_integration_test_docker_environment.lib.logging import luigi_log_config


def get_commit_sha_for_docker_tag(commit_sha: str) -> str:
    """
    Docker tags have a max len of 128 characters. If the commit sha is > 7 char, it'll be reduced to 7 chars.
    """
    if len(commit_sha) > 7:
        return commit_sha[:7]
    return commit_sha


class CIPrepare:

    def prepare(self, commit_sha: str):
        log_path = Path(DEFAULT_OUTPUT_DIRECTORY) / "jobs" / "logs" / "main.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        os.environ[luigi_log_config.LOG_ENV_VARIABLE_NAME] = f"{log_path.absolute()}"

        security_scan_path = Path(DEFAULT_OUTPUT_DIRECTORY) / "security_scan"
        meta_data_path = Path(DEFAULT_OUTPUT_DIRECTORY) / "meta_data"
        security_scan_path.mkdir(parents=True, exist_ok=True)
        meta_data_path.mkdir(parents=True, exist_ok=True)

        with open(meta_data_path / "start_date", "w") as f:
            f.write(datetime.now().isoformat())

        with open(meta_data_path / "commit_sha", "w") as f:
            f.write(commit_sha)
