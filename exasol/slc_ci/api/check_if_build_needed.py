from exasol.slc_ci.lib.check_if_build_needed import (
    check_if_need_to_build as lib_check_if_need_to_build,
)
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.model.build_config import BuildConfig


def check_if_build_needed(
    flavor: str, build_config: BuildConfig, branch_name: str
) -> bool:

    git_access: GitAccess = GitAccess()
    return lib_check_if_need_to_build(
        branch_name=branch_name,
        build_config=build_config,
        flavor=flavor,
        git_access=git_access,
    )
