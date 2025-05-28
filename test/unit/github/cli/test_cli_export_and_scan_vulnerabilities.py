from test.unit.github.cli.cli_runner import CliRunner
from test.unit.github.cli.is_instance_matcher import IsInstance
from unittest.mock import MagicMock, call

import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.export_and_scan_vulnerabilities as lib_export_and_scan_vulnerabilities
from exasol.slc_ci.cli.commands.export_and_scan_vulnerabilities import (
    export_and_scan_vulnerabilities,
)
from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_export import CIExport
from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_push import CIPush
from exasol.slc_ci.lib.ci_security_scan import CISecurityScan
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.lib.github_access import GithubAccess


@pytest.fixture
def cli():
    return CliRunner(export_and_scan_vulnerabilities)


@pytest.fixture
def mock_export_and_scan_vulnerabilities(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(
        lib_export_and_scan_vulnerabilities,
        "export_and_scan_vulnerabilities",
        mock_function_to_mock,
    )
    return mock_function_to_mock


def test_export_and_scan_vulnerabilities_no_flavor(cli):
    assert cli.run().failed and "Missing option '--flavor'" in cli.output


def test_export_and_scan_vulnerabilities_no_branch_name(cli):
    assert (
        cli.run("--flavor", "abc").failed
        and "Missing option '--branch-name'" in cli.output
    )


def test_export_and_scan_vulnerabilities_no_commit_sha(cli):
    assert (
        cli.run("--flavor", "abc", "--branch-name", "feature/abc").failed
        and "Missing option '--commit-sha'" in cli.output
    )


def test_export_and_scan_vulnerabilities_no_docker_user(cli):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--branch-name",
            "feature/abc",
            "--commit-sha",
            "12345",
        ).failed
        and "Missing option '--docker-user'" in cli.output
    )


def test_export_and_scan_vulnerabilities_no_docker_pwd(cli):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--branch-name",
            "feature/abc",
            "--commit-sha",
            "12345",
            "--docker-user",
            "user",
        ).failed
        and "Missing option '--docker-password'" in cli.output
    )


def test_export_and_scan_vulnerabilities_no_github_output_var(
    cli, mock_export_and_scan_vulnerabilities
):
    assert (
        cli.run(
            "--flavor",
            "abc",
            "--branch-name",
            "feature/abc",
            "--commit-sha",
            "12345",
            "--docker-user",
            "user",
            "--docker-password",
            "secret",
        ).failed
        and "Missing option '--github-output-var'" in cli.output
    )


TEST_DATA = [(None, False), ("--no-release", False), ("--release", True)]


@pytest.mark.parametrize("release_cli_option, expected_release_value", TEST_DATA)
def test_export_and_scan_vulnerabilities(
    cli,
    mock_export_and_scan_vulnerabilities,
    release_cli_option,
    expected_release_value,
):

    args = [
        "--flavor",
        "flavor_a",
        "--branch-name",
        "feature/abc",
        "--commit-sha",
        "12345",
        "--docker-user",
        "user",
        "--docker-password",
        "secret",
        "--github-output-var",
        "some_var",
    ]
    if release_cli_option is not None:
        args.append(release_cli_option)

    cli.run(*args)
    assert cli.succeeded

    # Validate the exact call using mock_calls and IsInstance matcher
    expected_call = call(
        release=expected_release_value,
        flavor="flavor_a",
        branch_name="feature/abc",
        docker_user="user",
        docker_password="secret",
        commit_sha="12345",
        git_access=IsInstance(GitAccess),
        github_access=IsInstance(GithubAccess),
        ci_build=IsInstance(CIBuild),
        ci_security_scan=IsInstance(CISecurityScan),
        ci_prepare=IsInstance(CIPrepare),
        ci_export=IsInstance(CIExport),
        ci_push=IsInstance(CIPush),
    )
    assert mock_export_and_scan_vulnerabilities.mock_calls == [expected_call]
