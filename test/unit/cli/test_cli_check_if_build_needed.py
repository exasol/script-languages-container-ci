from test.unit.cli.cli_runner import CliRunner
from test.unit.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.check_if_build_needed as lib_check_if_build_needed
from exasol.slc_ci.cli.commands.check_if_build_needed import check_if_build_needed
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.lib.github_access import GithubAccess
from exasol.slc_ci.model.github_event import GithubEvent


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


def test_check_if_build_needed_no_base_branch_name(cli):
    assert (
        cli.run("--flavor", "abc").failed
        and "Missing option '--base-ref'" in cli.output
    )


def test_check_if_build_needed_no_github_event(cli):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--base-ref",
            "master",
        ).failed
        and "Missing option '--github-event'" in cli.output
    )


def test_check_if_build_needed_no_github_var(cli):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--base-ref",
            "master",
            "--github-event",
            GithubEvent.PULL_REQUEST.value,
        ).failed
        and "Missing option '--github-output-var'" in cli.output
    )


def test_check_if_build_needed(cli, mock_check_if_build_needed):
    cli.run(
        "--flavor",
        "flavor_a",
        "--base-ref",
        "master",
        "--github-event",
        GithubEvent.PULL_REQUEST.value,
        "--github-output-var",
        "abc",
    )
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(
        flavor="flavor_a",
        base_ref="master",
        remote="origin",
        github_event=GithubEvent.PULL_REQUEST,
        github_access=IsInstance(GithubAccess),
        git_access=IsInstance(GitAccess),
    )
    assert mock_check_if_build_needed.mock_calls == [expected_call]
