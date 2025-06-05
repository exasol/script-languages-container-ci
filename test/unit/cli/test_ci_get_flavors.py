from test.unit.cli.cli_runner import CliRunner
from test.unit.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.get_flavors as lib_get_flavors
from exasol.slc_ci.cli.commands.get_flavors import get_flavors
from exasol.slc_ci.lib.github_access import GithubAccess


@pytest.fixture
def cli():
    return CliRunner(get_flavors)


@pytest.fixture
def mock_get_flavors(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(lib_get_flavors, "get_flavors", mock_function_to_mock)
    return mock_function_to_mock


def test_get_flavors_no_github_var(cli):
    assert cli.run().failed and "Missing option '--github-output-var'" in cli.output


def test_get_flavors(cli, mock_get_flavors):
    cli.run("--github-output-var", "abc")
    assert cli.succeeded
    expected_call = call(github_access=IsInstance(GithubAccess))
    assert mock_get_flavors.mock_calls == [expected_call]
