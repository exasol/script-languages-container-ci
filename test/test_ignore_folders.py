import json
from pathlib import Path
from typing import List

import pytest
from _pytest.tmpdir import TempPathFactory

from exasol_script_languages_container_ci.lib.ci import check_if_need_to_build
from exasol_script_languages_container_ci.lib.git_access import GitAccess
from test.fixtures import tmp_test_dir
import git


def commit_base(repo: git.Repo, repo_path: Path) -> None:
    """
    Create dummy commit on base branch with "something"
    """
    assert str(repo.active_branch) == "master"
    (repo_path / "something").parent.mkdir(parents=True, exist_ok=True)
    open(repo_path / "something", 'w').close()
    repo.index.add([str(repo_path / "something")])
    repo.index.commit("Base commit")


def commit_files(branch_name: str, repo: git.Repo, repo_path: Path,
                 files_to_commit: List[List[str]], commit_message: str) -> None:
    """
    Create empty given files (param files_to_commit) and commit them to a "Dummy commit"
    """
    commit_base(repo, repo_path)
    current = repo.create_head(branch_name)
    current.checkout()
    for file_list in files_to_commit:
        for file in file_list:
            (repo_path / file).parent.mkdir(parents=True, exist_ok=True)
            open(repo_path / file, 'w').close()
            repo.index.add([str(repo_path / file)])
        repo.index.commit(commit_message)


@pytest.fixture
def build_config(tmp_path_factory: TempPathFactory):
    config_path = tmp_path_factory.mktemp("build_config") / "build_config.json"
    with open(config_path, "w") as f:
        config = {"build_ignore": {"ignored_paths": ["doc", "githooks"]}, "base_branch": "master"}
        json.dump(config, f)
    return config_path


TEST_FLAVOR = "flavor_xyz"

TEST_DATA = [
    # If the last commit contains files not included in the ignore-path list, the build must run
    ("refs/heads/feature_branch",
     [["flavors/flavor_abc/build_steps.py", "doc/something", "src/udfclient.cpp"]], "message", True),
    # If there are 2 commits, and the last only contains files in the ignore-list, but the first contains
    # files not included in the ignore-path list, the build must run
    ("refs/heads/feature_branch",
     [["flavors/flavor_abc/build_steps.py", "doc/something", "src/udfclient.cpp"], ["doc/something"]], "message", True),
    # If last commit(s) contain only files included in the ignore-path-list the build must not run
    ("refs/heads/feature_branch",
     [["flavors/flavor_abc/build_steps.py", "doc/something"]], "message", False),
    # If last commit message contains "[rebuild]" the build should always trigger
    ("refs/heads/feature_branch",
     [["flavors/flavor_abc/build_steps.py", "doc/something"]], "message [rebuild]", True),
    # Affected files on current flavor should trigger a build
    ("refs/heads/feature_branch",
     [[f"flavors/{TEST_FLAVOR}/build_steps.py", "doc/something"]], "message", True),
    # If there are 2 commits, and the last only contains files in the ignore-list, but the first contains
    # files of the current flavor, the build must run
    ("refs/heads/feature_branch",
     [[f"flavors/{TEST_FLAVOR}/build_steps.py"], ["flavors/flavor_abc/build_steps.py"]], "message", True),
    ("refs/heads/develop", [["doc/something"]], "message", True), #Even if folder should be ignored, in case of develop branch we always expect to run
    ("refs/heads/master", [["doc/something"]], "message", True), #Even if folder should be ignored, in case of master branch we always expect to run
    ("refs/heads/main", [["doc/something"]], "message", True), #Even if folder should be ignored, in case of main branch we always expect to run
    ("refs/heads/rebuild/feature_branch", [["doc/something"]], "message", True), #Even if folder should be ignored, in case of rebuild/* branch we always expect to run
]


@pytest.mark.parametrize("branch_name, files_to_commit,commit_message, expected_result", TEST_DATA)
def test_ignore_folder_should_run_ci(branch_name, tmp_test_dir, build_config, files_to_commit,
                                     commit_message, expected_result):
    """
    This test creates a temporary git repository, commits the given file list (files_for_commit), then runs
    ci.check_if_need_to_build() and checks if it returned the expected result
    """
    repo_path = Path(tmp_test_dir)
    tmp_repo = git.Repo.init(repo_path)
    commit_files(branch_name, tmp_repo, repo_path, files_to_commit, commit_message)
    assert check_if_need_to_build(branch_name, str(build_config), TEST_FLAVOR, GitAccess()) == expected_result

