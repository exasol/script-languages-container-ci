import pytest
from _pytest.monkeypatch import MonkeyPatch

from exasol.slc_ci.cli.commands.check_if_build_needed import check_if_build_needed
from exasol_script_languages_container_ci.lib.git_access import GitAccess
from test.unit.github.cli.cli_runner import CliRunner
from unittest.mock import MagicMock
import exasol.slc_ci.lib.check_if_build_needed as lib_check_if_build_needed

@pytest.fixture
def cli():
    return CliRunner(check_if_build_needed)


@pytest.fixture
def mock_check_if_build_needed(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(lib_check_if_build_needed, "check_if_need_to_build", mock_function_to_mock)
    return mock_function_to_mock

def test_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_no_branch_name(cli):
    assert cli.run('--flavor', "abc").failed and "Missing option '--branch-name'" in cli.output

def test_no_github_var(cli):
    assert cli.run('--flavor', "abc", '--branch-name', 'feature/abc').failed and "Missing option '--github-var'" in cli.output

def test_check_if_build_needed(cli, mock_check_if_build_needed):
    cli.run('--flavor', 'flavor_a', '--branch-name', 'feature/abc', "--github-var", "abc")
    assert cli.succeeded
    assert mock_check_if_build_needed.call_count == 1
    assert mock_check_if_build_needed.call_args.kwargs["branch_name"] == "feature/abc"
    assert mock_check_if_build_needed.call_args.kwargs["flavor"] == "flavor_a"
    assert mock_check_if_build_needed.call_args.kwargs["github_var"] == "abc"
    assert isinstance(
        mock_check_if_build_needed.call_args.kwargs["git_access"], GitAccess
    )
