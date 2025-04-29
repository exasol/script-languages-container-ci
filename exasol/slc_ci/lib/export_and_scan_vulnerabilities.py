import logging
from pathlib import Path

from exasol.slc_ci.lib.branch_config import BranchConfig
from exasol.slc_ci.lib.ci_build import CIBuild
from exasol.slc_ci.lib.ci_export import CIExport
from exasol.slc_ci.lib.ci_prepare import CIPrepare
from exasol.slc_ci.lib.ci_push import CIPush
from exasol.slc_ci.lib.ci_security_scan import CISecurityScan
from exasol.slc_ci.lib.git_access import GitAccess
from exasol.slc_ci.model.build_config import BuildConfig


def export_and_scan_vulnerabilities(
    flavor: str,
    branch_name: str,
    docker_user: str,
    docker_password: str,
    commit_sha: str,
    build_config: BuildConfig,
    git_access: GitAccess,
    ci_build: CIBuild = CIBuild(),
    ci_security_scan: CISecurityScan = CISecurityScan(),
    ci_prepare: CIPrepare = CIPrepare(),
    ci_export: CIExport = CIExport(),
    ci_push: CIPush = CIPush(),
) -> Path:
    logging.info(
        f"Running build image and scan vulnerabilities for parameters: {locals()}"
    )

    flavor_path = (f"{build_config.flavors_path}/{flavor}",)
    test_container_folder = build_config.test_container_folder
    rebuild = BranchConfig.rebuild(branch_name)
    ci_prepare.prepare()
    ci_build.build(
        flavor_path=flavor_path,
        rebuild=rebuild,
        build_docker_repository=build_config.docker_build_repository,
        commit_sha=commit_sha,
        docker_user=docker_user,
        docker_password=docker_password,
        test_container_folder=test_container_folder,
    )
    ci_security_scan.run_security_scan(flavor_path=flavor_path)
    ci_push.push(
        flavor_path=flavor_path,
        target_docker_repository=build_config.docker_build_repository,
        target_docker_tag_prefix=commit_sha,
        docker_user=docker_user,
        docker_password=docker_password,
    )
    ci_push.push(
        flavor_path=flavor_path,
        target_docker_repository=build_config.docker_build_repository,
        target_docker_tag_prefix="",
        docker_user=docker_user,
        docker_password=docker_password,
    )
    return ci_export.export(flavor_path=flavor_path)
