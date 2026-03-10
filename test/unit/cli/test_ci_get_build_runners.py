from test.unit.cli.cli_runner import CliRunner
from test.unit.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.get_build_runners as lib_get_build_runners
from exasol.slc_ci.cli.commands.get_build_runners import get_build_runners
from exasol.slc_ci.lib.github_access import GithubAccess


@pytest.fixture
def cli():
    return CliRunner(get_build_runners)


@pytest.fixture
def mock_get_build_runners(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(
        lib_get_build_runners, "get_build_runners", mock_function_to_mock
    )
    return mock_function_to_mock


def test_get_build_runners_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_get_build_runners_no_github_var(cli):
    assert (
        cli.run("--flavor", "abc").failed
        and "Missing option '--github-output-var'" in cli.output
    )


def test_get_build_runners(cli, mock_get_build_runners):
    cli.run("--flavor", "flavor_a", "--github-output-var", "abc")
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(flavor="flavor_a", github_access=IsInstance(GithubAccess))
    assert mock_get_build_runners.mock_calls == [expected_call]
