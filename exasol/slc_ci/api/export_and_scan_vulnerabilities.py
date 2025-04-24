from pathlib import Path

from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_export import CIExport
from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_push import CIPush
from exasol.slc_ci.lib.ci_security_scan import CISecurityScan
from exasol.slc_ci.lib.export_and_scan_vulnerabilities import (
    export_and_scan_vulnerabilities as lib_export_and_scan_vulnerabilities,
)
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.model.build_config import BuildConfig


def export_and_scan_vulnerabilities(
    flavor: str,
    build_config: BuildConfig,
    branch_name: str,
    docker_user: str,
    docker_password: str,
    commit_sha: str,
) -> Path:
    git_access: GitAccess = GitAccess()
    ci_build: CIBuild = CIBuild()
    ci_security_scan: CISecurityScan = CISecurityScan()
    ci_prepare: CIPrepare = CIPrepare()
    ci_export: CIExport = CIExport()
    ci_push: CIPush = CIPush()

    return lib_export_and_scan_vulnerabilities(
        flavor=flavor,
        branch_name=branch_name,
        docker_user=docker_user,
        docker_password=docker_password,
        commit_sha=commit_sha,
        build_config=build_config,
        git_access=git_access,
        ci_build=ci_build,
        ci_security_scan=ci_security_scan,
        ci_prepare=ci_prepare,
        ci_export=ci_export,
        ci_push=ci_push,
    )
