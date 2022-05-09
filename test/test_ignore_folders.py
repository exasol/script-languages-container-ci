import json
from pathlib import Path
from typing import List

import pytest
from _pytest.tmpdir import TempPathFactory

from exasol_script_languages_container_ci.lib.ci import check_if_need_to_build
from exasol_script_languages_container_ci.lib.git_access import GitAccess
from test.fixtures import tmp_test_dir
import git


def commit_files(repo: git.Repo, repo_path: Path, files_to_commit: List[str]):
    """
    Create empty given files (param files_to_commit) and commit them to a "Dummy commit"
    """
    for file in files_to_commit:
        (repo_path / file).parent.mkdir(parents=True, exist_ok=True)
        open(repo_path / file, 'w').close()
        repo.index.add([str(repo_path / file)])
    repo.index.commit("Dummy commit")


@pytest.fixture
def build_config(tmp_path_factory: TempPathFactory):
    config_path = tmp_path_factory.mktemp("build_config") / "build_config.json"
    with open(config_path, "w") as f:
        config = {"build_ignore": {"ignored_paths": ["doc", "githooks"]}}
        json.dump(config, f)
    return config_path


TEST_FLAVOR = "flavor_xyz"

TEST_DATA = [
    (["flavors/flavor_abc/build_steps.py", "doc/something", "src/udfclient.cpp"], True),
    (["flavors/flavor_abc/build_steps.py", "doc/something"], False),
    ([f"flavors/{TEST_FLAVOR}/build_steps.py", "doc/something"], True)
]


@pytest.mark.parametrize("files_to_commit,expected_result", TEST_DATA)
def test_ignore_folder_should_run_ci(tmp_test_dir, build_config, files_to_commit, expected_result):
    """
    This test creates a temporary git repository, commits the given file list (files_for_commit), then runs
    ci.check_if_need_to_build() and checks if it returned the expected result
    """
    repo_path = Path(tmp_test_dir)
    tmp_repo = git.Repo.init(repo_path)
    commit_files(tmp_repo, repo_path, files_to_commit)
    assert check_if_need_to_build(str(build_config), TEST_FLAVOR, GitAccess()) == expected_result

