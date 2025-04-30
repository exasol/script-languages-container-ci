import logging
from typing import Set

from exasol.slc_ci.lib.branch_config import BranchConfig
from exasol.slc_ci.lib.get_build_config_model import get_build_config_model
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.lib.github_access import GithubAccess


def get_all_affected_files(git_access: GitAccess, base_branch: str) -> Set[str]:
    base_last_commit_sha = git_access.get_head_commit_sha_of_branch(base_branch)
    changed_files = set()  # type: ignore
    for commit in git_access.get_last_commits():
        if commit == base_last_commit_sha:
            break
        changed_files.update(git_access.get_files_of_commit(commit))
    return changed_files


def _run_check_if_need_to_build(
    branch_name: str, flavor: str, git_access: GitAccess
) -> bool:
    build_config = get_build_config_model()
    if BranchConfig.build_always(branch_name):
        return True
    if "[rebuild]" in git_access.get_last_commit_message():
        return True
    affected_files = list(get_all_affected_files(git_access, build_config.base_branch))
    logging.debug(
        f"check_if_need_to_build: Found files of last commits: {affected_files}"
    )
    for ignore_path in build_config.ignore_paths:
        affected_files = list(
            filter(lambda file: not file.startswith(ignore_path), affected_files)
        )

    if len(affected_files) > 0:
        # Now filter out also other flavor folders
        this_flavor_path = f"flavors/{flavor}"
        affected_files = list(
            filter(
                lambda file: not file.startswith("flavors")
                or file.startswith(this_flavor_path),
                affected_files,
            )
        )
    logging.debug(f"check_if_need_to_build: filtered files: {affected_files}")
    return len(affected_files) > 0

def check_if_need_to_build(
    branch_name: str, flavor: str, github_access: GithubAccess, git_access: GitAccess
) -> None:
    res = _run_check_if_need_to_build(branch_name, flavor, git_access)
    github_access.write_result("True" if res else "False")
