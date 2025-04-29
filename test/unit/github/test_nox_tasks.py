import argparse
import sys
from pathlib import Path
from test.unit.github.test_env import test_env
from unittest import mock
from unittest.mock import MagicMock

import nox
import pytest
from _pytest.monkeypatch import MonkeyPatch

import exasol.slc_ci.lib.check_if_build_needed as lib_check_if_build_needed
import exasol.slc_ci.lib.get_flavor_ci_model as lib_get_flavor_ci_model
import exasol.slc_ci.lib.get_flavors as lib_get_flavors
from exasol.slc_ci.lib.git_access import GitAccess

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
    monkeypatch.setattr(lib_get_flavors, "get_flavors", mock_function_to_mock)
    return mock_function_to_mock


@pytest.fixture
def mock_get_flavor_ci_model(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock(return_value=test_env.flavor_config)
    monkeypatch.setattr(
        lib_get_flavor_ci_model, "get_flavor_ci_model", mock_function_to_mock
    )
    return mock_function_to_mock


@pytest.fixture
def mock_check_if_build_needed(monkeypatch: MonkeyPatch) -> MagicMock:
    mock_function_to_mock = MagicMock(return_value=True)
    monkeypatch.setattr(
        lib_check_if_build_needed, "check_if_need_to_build", mock_function_to_mock
    )
    return mock_function_to_mock


@pytest.fixture
def fake_session_builder():
    def fake_session(session_name: str, *args):
        global_config = argparse.Namespace(posargs=args)
        session_runner = nox.sessions.SessionRunner(
            name=session_name,
            signatures=[],
            func=None,  # type: ignore
            global_config=global_config,
            manifest=None,  # type: ignore
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
        build_config=nox_tasks.SLC_BUILD_CONFIG
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
        build_config=nox_tasks.SLC_BUILD_CONFIG, flavor="flavor_a"
    )
    out_content = github_output.read_text()
    assert out_content == """test=some_build_runner\n"""


def test_run_check_if_build_needed(
    fake_session_builder, nox_tasks, mock_check_if_build_needed, github_output
) -> None:
    fake_session = fake_session_builder(
        nox_tasks.run_check_if_build_needed.name,
        "--flavor",
        "flavor_a",
        "--branch-name",
        "feature/abc",
        "--github-var",
        "test",
    )
    nox_tasks.run_check_if_build_needed(fake_session)
    assert mock_check_if_build_needed.call_count == 1
    assert mock_check_if_build_needed.call_args.kwargs["branch_name"] == "feature/abc"
    assert (
        mock_check_if_build_needed.call_args.kwargs["build_config"]
        == nox_tasks.SLC_BUILD_CONFIG
    )
    assert mock_check_if_build_needed.call_args.kwargs["flavor"] == "flavor_a"
    assert isinstance(
        mock_check_if_build_needed.call_args.kwargs["git_access"], GitAccess
    )
    out_content = github_output.read_text()
    assert out_content == """test=True\n"""
