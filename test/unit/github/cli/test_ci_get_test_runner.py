from test.unit.github.cli.cli_runner import CliRunner
from test.unit.github.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.get_test_runner as lib_get_test_runner
from exasol.slc_ci.cli.commands.get_test_runner import get_test_runner
from exasol.slc_ci.lib.github_access import GithubAccess


@pytest.fixture
def cli():
    return CliRunner(get_test_runner)


@pytest.fixture
def mock_get_test_runner(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(lib_get_test_runner, "get_test_runner", mock_function_to_mock)
    return mock_function_to_mock


def test_get_test_runner_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_get_test_runner_no_test_set_name(cli):
    assert (
        cli.run("--flavor", "abc").failed
        and "Missing option '--test-set-name'" in cli.output
    )


def test_get_test_runner_no_github_var(cli):
    assert (
        cli.run("--flavor", "abc", "--test-set-name", "all").failed
        and "Missing option '--github-output-var'" in cli.output
    )


def test_get_test_runner(cli, mock_get_test_runner):
    cli.run(
        "--flavor", "flavor_a", "--test-set-name", "all", "--github-output-var", "abc"
    )
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(
        flavor="flavor_a", test_set_name="all", github_access=IsInstance(GithubAccess)
    )
    assert mock_get_test_runner.mock_calls == [expected_call]
