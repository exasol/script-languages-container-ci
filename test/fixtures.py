from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

import click
import pytest


@pytest.fixture
def build_output_dir():
    with TemporaryDirectory() as temp_dir:
        security_scan_dir = Path(temp_dir) / ".build_output" / "security_scan"
        security_scan_dir.mkdir(parents=True, exist_ok=False)
        security_report = open(security_scan_dir / "security_report", "w")
        yield temp_dir


@pytest.fixture
def click_stub():
    click_ctx = click.Context(command=click.Command("dummy"))
    return Mock(click_ctx)


class TestEnv:
    def __init__(self, docker_user, docker_pwd, docker_build_repo, docker_release_repo, commit_sha):
        self.docker_user = docker_user
        self.docker_pwd = docker_pwd
        self.docker_release_repo = docker_build_repo
        self.docker_build_repo = docker_build_repo
        self.commit_sha = commit_sha


@pytest.fixture
def test_env():
    return TestEnv(docker_user="test_docker_user", docker_pwd="test_docker_pwd",
                   docker_build_repo="test_docker_build_repo", docker_release_repo="test_docker_release_repo",
                   commit_sha="test_commit_sha")