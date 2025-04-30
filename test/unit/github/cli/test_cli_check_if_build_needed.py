from test.unit.github.cli.cli_runner import CliRunner
from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.check_if_build_needed as lib_check_if_build_needed
from exasol.slc_ci.cli.commands.check_if_build_needed import check_if_build_needed
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.lib.github_access import GithubAccess


@pytest.fixture
def cli():
    return CliRunner(check_if_build_needed)


@pytest.fixture
def mock_check_if_build_needed(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(
        lib_check_if_build_needed, "check_if_need_to_build", mock_function_to_mock
    )
    return mock_function_to_mock


def test_check_if_build_needed_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_check_if_build_needed_no_branch_name(cli):
    assert (
        cli.run("--flavor", "abc").failed
        and "Missing option '--branch-name'" in cli.output
    )


def test_check_if_build_needed_no_base_branch_name(cli):
    assert (
        cli.run("--flavor", "abc", "--branch-name", "feature/abc").failed
        and "Missing option '--base-branch-name'" in cli.output
    )


def test_check_if_build_needed_no_github_var(cli):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--branch-name",
            "feature/abc",
            "--base-branch-name",
            "master",
        ).failed
        and "Missing option '--github-var'" in cli.output
    )


def test_check_if_build_needed(cli, mock_check_if_build_needed):
    cli.run(
        "--flavor",
        "flavor_a",
        "--branch-name",
        "feature/abc",
        "--base-branch-name",
        "master",
        "--github-var",
        "abc",
    )
    assert cli.succeeded
    assert mock_check_if_build_needed.call_count == 1
    assert len(mock_check_if_build_needed.call_args.args) == 0
    assert len(mock_check_if_build_needed.call_args.kwargs) == 5
    assert mock_check_if_build_needed.call_args.kwargs["branch_name"] == "feature/abc"
    assert mock_check_if_build_needed.call_args.kwargs["base_branch_name"] == "master"
    assert mock_check_if_build_needed.call_args.kwargs["flavor"] == "flavor_a"
    assert isinstance(
        mock_check_if_build_needed.call_args.kwargs["github_access"], GithubAccess
    )
    assert isinstance(
        mock_check_if_build_needed.call_args.kwargs["git_access"], GitAccess
    )
