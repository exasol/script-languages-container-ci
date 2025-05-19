from test.unit.github.cli.cli_runner import CliRunner
from test.unit.github.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.run_tests as lib_run_tests
from exasol.slc_ci.cli.commands import run_tests
from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_test import CIExecuteTest


@pytest.fixture
def cli():
    return CliRunner(run_tests)


@pytest.fixture
def mock_run_tests(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(
        lib_run_tests,
        "run_tests",
        mock_function_to_mock,
    )
    return mock_function_to_mock


def test_run_tests_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_run_tests_no_slc_directory(cli):
    assert (
        cli.run("--flavor", "abc").failed
        and "Missing option '--slc-directory'" in cli.output
    )


def test_run_tests_no_test_set_name(cli):
    assert (
        cli.run("--flavor", "abc", "--slc-directory", "some_dir").failed
        and "Missing option '--test-set-name'" in cli.output
    )


def test_run_tests_no_docker_user(cli):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--slc-directory",
            "some_dir",
            "--test-set-name",
            "all",
        ).failed
        and "Missing option '--docker-user'" in cli.output
    )


def test_run_tests_no_docker_pwd(cli):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--slc-directory",
            "some_dir",
            "--test-set-name",
            "all",
            "--docker-user",
            "user",
        ).failed
        and "Missing option '--docker-password'" in cli.output
    )


def test_run_tests(cli, mock_run_tests):
    cli.run(
        "--flavor",
        "flavor_a",
        "--slc-directory",
        "some_dir",
        "--test-set-name",
        "all",
        "--docker-user",
        "user",
        "--docker-password",
        "secret",
    )
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(
        flavor="flavor_a",
        slc_directory="some_dir",
        test_set_name="all",
        docker_user="user",
        docker_password="secret",
        ci_prepare=IsInstance(CIPrepare),
        ci_test=IsInstance(CIExecuteTest),
    )
    assert mock_run_tests.mock_calls == [expected_call]
