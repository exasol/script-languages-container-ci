from pathlib import Path
from typing import List
from unittest.mock import MagicMock

import git
import pytest

from exasol.slc_ci.lib.check_if_build_needed import check_if_need_to_build
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.model.build_mode import BuildMode


def commit_base(repo: git.Repo, repo_path: Path) -> None:
    """
    Create dummy commit on base branch with "something"
    """
    (repo_path / "something").parent.mkdir(parents=True, exist_ok=True)
    open(repo_path / "something", "w").close()
    repo.index.add([str(repo_path / "something")])
    repo.index.commit("Base commit")
    assert repo.active_branch.name == "master" or repo.active_branch.name == "main"
    if repo.active_branch.name == "main":
        repo.active_branch.rename("master")


def commit_files(
    repo: git.Repo,
    repo_path: Path,
    files_to_commit: list[list[str]],
    commit_message: str,
) -> None:
    """
    Create empty given files (param files_to_commit) and commit them to a "Dummy commit"
    """
    commit_base(repo, repo_path)
    current = repo.create_head("feature_abc")
    current.checkout()
    for file_list in files_to_commit:
        for file in file_list:
            (repo_path / file).parent.mkdir(parents=True, exist_ok=True)
            open(repo_path / file, "w").close()
            repo.index.add([str(repo_path / file)])
        repo.index.commit(commit_message)


TEST_FLAVOR = "flavor_xyz"


TEST_DATA = [
    # If the last commit contains files not included in the ignore-path list, the build must run
    (
        "last_commit_not_ignore_path_build_must_run",
        [["flavors/flavor_abc/build_steps.py", "doc/something", "src/udfclient.cpp"]],
        "message",
        "pull_request",
        BuildMode.NORMAL.value,
    ),
    # If there are 2 commits, and the last only contains files in the ignore-list, but the first contains
    # files not included in the ignore-path list, the build must run
    (
        "commit_before_last_commit_not_ignore_path_build_must_run",
        [
            ["flavors/flavor_abc/build_steps.py", "doc/something", "src/udfclient.cpp"],
            ["doc/something"],
        ],
        "message",
        "pull_request",
        BuildMode.NORMAL.value,
    ),
    # If last commit(s) contain only files included in the ignore-path-list or another flavor the build must not run
    (
        "last_commit_ignore_path_or_another_flavor_build_must_not_run",
        [["flavors/flavor_abc/build_steps.py", "doc/something"]],
        "message",
        "pull_request",
        BuildMode.NO_BUILD_NEEDED.value,
    ),
    # If last commit message contains "[rebuild]" the build should always trigger
    (
        "rebuild_in_last_commit_msg_build_must_run",
        [["flavors/flavor_abc/build_steps.py", "doc/something"]],
        "message [rebuild]",
        "pull_request",
        BuildMode.NORMAL.value,
    ),
    # Affected files on current flavor should trigger a build
    (
        "changes_in_current_flavor_build_must_run",
        [[f"flavors/{TEST_FLAVOR}/build_steps.py", "doc/something"]],
        "message",
        "pull_request",
        BuildMode.NORMAL.value,
    ),
    # If there are 2 commits, and the last only contains files in the ignore-list, but the first contains
    # files of the current flavor, the build must run
    (
        "changes_in_current_flavor_before_last_commit_build_must_run",
        [
            [f"flavors/{TEST_FLAVOR}/build_steps.py"],
            ["flavors/flavor_abc/build_steps.py"],
        ],
        "message",
        "pull_request",
        BuildMode.NORMAL.value,
    ),
    (
        "push_event",
        [
            [f"flavors/{TEST_FLAVOR}/build_steps.py"],
            ["flavors/flavor_abc/build_steps.py"],
        ],
        "message",
        "push",
        BuildMode.REBUILD.value,
    ),
]


@pytest.mark.parametrize(
    "test_name, files_to_commit,commit_message, github_event, expected_result",
    TEST_DATA,
)
def test_ignore_folder_should_run_ci(
    build_config_environment,
    test_name: str,
    tmp_test_dir,
    files_to_commit,
    commit_message: str,
    github_event: str,
    expected_result: str,
):
    """
    This test creates a temporary git repository, commits the given file list (files_for_commit), then runs
    ci.check_if_need_to_build() and checks if it returned the expected result
    """
    github_output_mock = MagicMock()
    repo_path = Path(tmp_test_dir)
    tmp_repo = git.Repo.init(repo_path)
    commit_files(tmp_repo, repo_path, files_to_commit, commit_message)
    check_if_need_to_build(
        base_ref="master",
        remote="",
        flavor=TEST_FLAVOR,
        github_event=github_event,
        github_access=github_output_mock,
        git_access=GitAccess(),
    )

    assert github_output_mock.write_result.call_args.args[0] == expected_result
