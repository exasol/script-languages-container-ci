from test.unit.github.cli.cli_runner import CliRunner
from test.unit.github.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.prepare_test_container as lib_prepare_test_container
from exasol.slc_ci.cli.commands.prepare_test_container import prepare_test_container
from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_push_test_container import CIPushTestContainer


@pytest.fixture
def cli():
    return CliRunner(prepare_test_container)


@pytest.fixture
def mock_prepare_test_container(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(
        lib_prepare_test_container,
        "prepare_test_container",
        mock_function_to_mock,
    )
    return mock_function_to_mock


def test_prepare_test_container_no_commit_sha(cli):
    assert cli.run().failed and "Missing option '--commit-sha'" in cli.output


def test_prepare_test_container_no_docker_user(cli):
    assert (
        cli.run(
            "--commit-sha",
            "12345",
        ).failed
        and "Missing option '--docker-user'" in cli.output
    )


def test_prepare_test_container_no_docker_pwd(cli):
    assert (
        cli.run(
            "--commit-sha",
            "12345",
            "--docker-user",
            "user",
        ).failed
        and "Missing option '--docker-password'" in cli.output
    )


def test_prepare_test_container(cli, mock_prepare_test_container):
    cli.run(
        "--commit-sha",
        "12345",
        "--docker-user",
        "user",
        "--docker-password",
        "secret",
    )
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(
        commit_sha="12345",
        docker_user="user",
        docker_password="secret",
        ci_push_test_container=IsInstance(CIPushTestContainer),
        ci_prepare=IsInstance(CIPrepare),
    )
    assert mock_prepare_test_container.mock_calls == [expected_call]
