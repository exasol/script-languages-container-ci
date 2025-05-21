from test.unit.github.cli.cli_runner import CliRunner
from test.unit.github.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.get_test_matrix as lib_get_test_matrix
from exasol.slc_ci.cli.commands.get_test_matrix import get_test_matrix
from exasol.slc_ci.lib.github_access import GithubAccess


@pytest.fixture
def cli():
    return CliRunner(get_test_matrix)


@pytest.fixture
def mock_get_test_matrix(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(lib_get_test_matrix, "get_test_matrix", mock_function_to_mock)
    return mock_function_to_mock


def test_get_test_matrix_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_get_test_matrix_no_github_var(cli):
    assert (
        cli.run("--flavor", "abc").failed
        and "Missing option '--github-output-var'" in cli.output
    )


def test_get_test_matrix(cli, mock_get_test_matrix):
    cli.run("--flavor", "flavor_a", "--github-output-var", "abc")
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(
        flavor="flavor_a", github_access=IsInstance(GithubAccess)
    )
    assert mock_get_test_matrix.mock_calls == [expected_call]
