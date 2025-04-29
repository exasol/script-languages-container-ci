import argparse
import sys
from pathlib import Path
from test.unit.v2.test_env import test_env
from unittest import mock
from unittest.mock import MagicMock

import nox
import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.api as api

FLAVORS = ["flavor_a", "flavor_b"]


@pytest.fixture(scope="module")
def nox_tasks():
    resources_path = Path(__file__).parent / "resources"
    # exasol.slc_ci.nox.tasks imports 'slc_build_config.py`. We must ensure that this modul can be found by adding it to the sys path.
    sys.path.append(str(resources_path))
    import exasol.slc_ci.nox.tasks as nox_tasks

    yield nox_tasks
    # now remove 'slc_build_config.py` again from sys path.
    sys.path.pop()


@pytest.fixture
def mock_get_flavors(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock(return_value=FLAVORS)
    monkeypatch.setattr(api, "get_flavors", mock_function_to_mock)
    return mock_function_to_mock


@pytest.fixture
def mock_get_flavor_ci_model(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock(return_value=test_env.flavor_config)
    monkeypatch.setattr(api, "get_flavor_ci_model", mock_function_to_mock)
    return mock_function_to_mock


@pytest.fixture
def mock_run_tests(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock(return_value=None)
    monkeypatch.setattr(api, "run_tests", mock_function_to_mock)
    return mock_function_to_mock


@pytest.fixture
def mock_check_if_build_needed(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock(return_value=True)
    monkeypatch.setattr(api, "check_if_build_needed", mock_function_to_mock)
    return mock_function_to_mock


@pytest.fixture
def mock_export_and_scan_vulnerabilities(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock(return_value="/tmp/slc.tar.gz")
    monkeypatch.setattr(api, "export_and_scan_vulnerabilities", mock_function_to_mock)
    return mock_function_to_mock


@pytest.fixture
def fake_session_builder():
    def fake_session(session_name: str, *args):
        global_config = argparse.Namespace(posargs=args)
        session_runner = nox.sessions.SessionRunner(
            name=session_name,
            signatures=[],
            func=None, #type: ignore
            global_config=global_config,
            manifest=None, #type: ignore
        )
        return nox.sessions.Session(session_runner)

    return fake_session


@pytest.fixture
def github_output(monkeypatch: MonkeyPatch, tmp_path):
    out_file = tmp_path / "out.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))
    return out_file


def test_run_find_available_flavors(
    fake_session_builder, nox_tasks, mock_get_flavors, github_output
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_find_available_flavors.name, "--github-var", "test"
    )
    nox_tasks.run_find_available_flavors(fake_session)
    assert mock_get_flavors.call_count == 1
    assert mock_get_flavors.call_args == mock.call(
        Path(__file__).parent / "resources" / "flavors"
    )
    out_content = github_output.read_text()
    assert out_content == """test=["flavor_a", "flavor_b"]\n"""


def test_run_get_build_runner_for_flavor(
    fake_session_builder, nox_tasks, mock_get_flavor_ci_model, github_output
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_get_build_runner_for_flavor.name,
        "--flavor",
        "flavor_a",
        "--github-var",
        "test",
    )
    nox_tasks.run_get_build_runner_for_flavor(fake_session)
    assert mock_get_flavor_ci_model.call_count == 1
    assert mock_get_flavor_ci_model.call_args == mock.call(
        nox_tasks.SLC_BUILD_CONFIG, "flavor_a"
    )
    out_content = github_output.read_text()
    assert out_content == """test=some_build_runner\n"""


def test_run_get_test_runner_for_flavor(
    fake_session_builder, nox_tasks, mock_get_flavor_ci_model, github_output
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_get_test_runner_for_flavor.name,
        "--flavor",
        "flavor_a",
        "--github-var",
        "test",
    )
    nox_tasks.run_get_test_runner_for_flavor(fake_session)
    assert mock_get_flavor_ci_model.call_count == 1
    assert mock_get_flavor_ci_model.call_args == mock.call(
        nox_tasks.SLC_BUILD_CONFIG, "flavor_a"
    )
    out_content = github_output.read_text()
    assert out_content == """test=some_test_runner\n"""


def test_run_get_test_set_names_for_flavor(
    fake_session_builder, nox_tasks, mock_get_flavor_ci_model, github_output
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_get_test_set_names_for_flavor.name,
        "--flavor",
        "flavor_a",
        "--github-var",
        "test",
    )
    nox_tasks.run_get_test_set_names_for_flavor(fake_session)
    assert mock_get_flavor_ci_model.call_count == 1
    assert mock_get_flavor_ci_model.call_args == mock.call(
        nox_tasks.SLC_BUILD_CONFIG, "flavor_a"
    )
    out_content = github_output.read_text()
    assert out_content == """test=["some_test_name"]\n"""


def test_run_db_tests(
    fake_session_builder, nox_tasks, mock_get_flavor_ci_model, mock_run_tests
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_db_tests.name,
        "--flavor",
        "flavor_a",
        "--docker-user",
        "some_user",
        "--docker-password",
        "super_secret",
        "--test-set-name",
        "all",
        "--slc-directory",
        "some_directory",
    )
    nox_tasks.run_db_tests(fake_session)
    assert mock_get_flavor_ci_model.call_count == 1
    assert mock_get_flavor_ci_model.call_args == mock.call(
        nox_tasks.SLC_BUILD_CONFIG, "flavor_a"
    )
    assert mock_run_tests.call_count == 1
    assert mock_run_tests.call_args == mock.call(
        flavor="flavor_a",
        slc_directory="some_directory",
        flavor_config=test_env.flavor_config,
        build_config=test_env.build_config,
        test_set_name="all",
        docker_user="some_user",
        docker_password="super_secret",
    )


def test_run_check_if_build_needed(
    fake_session_builder, nox_tasks, mock_check_if_build_needed, github_output
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_db_tests.name,
        "--flavor",
        "flavor_a",
        "--branch-name",
        "feature/abc",
        "--github-var",
        "test",
    )
    nox_tasks.run_check_if_build_needed(fake_session)
    assert mock_check_if_build_needed.call_count == 1
    assert mock_check_if_build_needed.call_args == mock.call(
        branch_name="feature/abc",
        flavor="flavor_a",
        build_config=nox_tasks.SLC_BUILD_CONFIG,
    )
    out_content = github_output.read_text()
    assert out_content == """test=True\n"""


def test_run_export_and_scan_vulnerabilities(
    fake_session_builder, nox_tasks, mock_export_and_scan_vulnerabilities, github_output
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_db_tests.name,
        "--flavor",
        "flavor_a",
        "--branch-name",
        "feature/abc",
        "--docker-user",
        "some_user",
        "--docker-password",
        "super_secret",
        "--commit-sha",
        "ABCDE",
        "--github-var",
        "test",
    )
    nox_tasks.run_export_and_scan_vulnerabilities(fake_session)
    assert mock_export_and_scan_vulnerabilities.call_count == 1
    assert mock_export_and_scan_vulnerabilities.call_args == mock.call(
        flavor="flavor_a",
        build_config=nox_tasks.SLC_BUILD_CONFIG,
        branch_name="feature/abc",
        docker_user="some_user",
        docker_password="super_secret",
        commit_sha="ABCDE",
    )
    out_content = github_output.read_text()
    assert out_content == """test=/tmp/slc.tar.gz\n"""
