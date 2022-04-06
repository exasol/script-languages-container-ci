import os

from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch, MagicMock

import click
import pytest
import exasol_script_languages_container_ci


@pytest.fixture(autouse=True)
def tmp_test_dir():
    """
    Change cwd to a tmp directory for executing tests. Thus, we avoid any possible interference (git repository).
    :return:
    """
    with TemporaryDirectory() as temp_dir:
        old_dir = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(old_dir)


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


@pytest.fixture(autouse=True)
def patch_printfile():
    """
    This overwrites automatically function "exasol_script_languages_container_ci.lib.print_file" because within the UnitTests
    the output files are not being created. Also accelerate Unit-Tests by avoiding file-access.
    """
    with patch('exasol_script_languages_container_ci.lib.print_file', MagicMock()):
        yield
