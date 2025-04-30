import pytest
from _pytest.monkeypatch import MonkeyPatch

from exasol.slc_ci.cli.commands.get_build_runner import get_build_runner
from exasol.slc_ci.lib.github_access import GithubAccess
from test.unit.github.cli.cli_runner import CliRunner
from unittest.mock import MagicMock
import exasol.slc_ci.lib.get_build_runner as lib_get_build_runner


@pytest.fixture
def cli():
    return CliRunner(get_build_runner)


@pytest.fixture
def mock_get_build_runner(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(lib_get_build_runner, "get_build_runner", mock_function_to_mock)
    return mock_function_to_mock

def test_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_no_github_var(cli):
    assert cli.run('--flavor', "abc").failed and "Missing option '--github-var'" in cli.output


def test_get_build_runner(cli, mock_get_build_runner):
    cli.run("--flavor", "flavor_a", "--github-var", "abc")
    assert cli.succeeded
    assert mock_get_build_runner.call_count == 1
    assert len(mock_get_build_runner.call_args.args) == 0
    assert len(mock_get_build_runner.call_args.kwargs.keys()) == 2

    assert mock_get_build_runner.call_args.kwargs["flavor"] == "flavor_a"
    assert isinstance(mock_get_build_runner.call_args.kwargs["github_access"], GithubAccess)

