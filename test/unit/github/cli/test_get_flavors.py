from unittest import mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from exasol.slc_ci.lib.github_access import GithubAccess
from test.unit.github.cli.cli_runner import CliRunner
from exasol.slc_ci.cli.commands.get_flavors import get_flavors
from unittest.mock import patch, MagicMock
import exasol.slc_ci.lib.get_flavors as lib_get_flavors

@pytest.fixture
def cli():
    return CliRunner(get_flavors)


@pytest.fixture
def mock_get_flavors(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(lib_get_flavors, "get_flavors", mock_function_to_mock)
    return mock_function_to_mock

def test_no_github_var(cli):
    assert cli.run().failed and "Missing option '--github-var'" in cli.output


def test_get_flavors(cli, mock_get_flavors):
    cli.run("--github-var", "abc")
    assert cli.succeeded
    assert mock_get_flavors.call_count == 1
    assert len(mock_get_flavors.call_args.args) == 0
    assert len(mock_get_flavors.call_args.kwargs) == 1
    assert isinstance(mock_get_flavors.call_args.kwargs["github_access"], GithubAccess)

