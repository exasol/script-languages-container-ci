import json
import platform
import shutil
from inspect import cleandoc
from pathlib import Path
from test.integration.tag_infos import (
    EXPECTED_TAG_INFO_HASHES,
    TagInfo,
    EXPECTED_TAG_INFO_RELEASE,
)

from exasol_integration_test_docker_environment.testing.docker_registry import (
    LocalDockerRegistryContextManager,
)

from exasol.slc_ci.lib.export_and_scan_vulnerabilities import (
    export_and_scan_vulnerabilities,
)
from exasol.slc_ci.model.build_mode import BuildMode


class TestGithubAccess:
    def __init__(self):
        self.result = None

    def write_result(self, result: str):
        self.result = result


def _build_tag_name_ci(
    commit_sha: str, flavor_name: str, arch: str, tag_info: TagInfo
) -> str:
    if commit_sha:
        return f"{commit_sha}_{flavor_name}-{tag_info.build_step}_{arch}_{tag_info.tag_suffix}"
    else:
        return f"{flavor_name}-{tag_info.build_step}_{arch}_{tag_info.tag_suffix}"

def _build_tag_name_cd(
    flavor_name: str, arch: str, branch_name: str, tag_info: TagInfo
) -> str:
    return f"{flavor_name}-{tag_info.build_step}_{arch}_{branch_name}"


def test_ci(flavors_path, tmp_test_dir: str):
    flavor_name = "successful"
    machine = platform.machine().lower()
    arch = "arm64" if ("arm" in machine) or ("aarch" in machine) else "x64"

    branch_name = "test_branch"
    docker_user = None
    docker_password = None

    commit_sha = "123"
    github_access = TestGithubAccess()

    shutil.copytree(src=flavors_path, dst=Path(tmp_test_dir) / "flavors")

    build_config_path = Path(tmp_test_dir) / "build_config.json"
    build_config_content = cleandoc("""
 {{
    "ignore_paths": [
      "some_path"
    ],
    "docker_build_repository": "{build_repository}",
    "docker_release_repository": "{release_repository}",
    "test_container_folder": "test_container"
}}
""")

    repository_name = "test_export_and_scan_vulnerabilities"
    release_hash = [tag_info.tag_suffix for tag_info in EXPECTED_TAG_INFO_HASHES if tag_info.build_step == "release"][0]
    test_hash = [
        tag_info.tag_suffix
        for tag_info in EXPECTED_TAG_INFO_HASHES
        if tag_info.build_step == "base_test_build_run"
    ][0]
    export_release_tar_gz_file = Path(tmp_test_dir) / ".build_output_release" / "cache" / "exports" / f"{flavor_name}-release-{arch}-{release_hash}.tar.gz" 
    export_test_tar_gz_file = Path(tmp_test_dir) / ".build_output_test" / "cache" / "exports" / f"{flavor_name}-base_test_build_run-{arch}-{test_hash}.tar.gz"
    exported_github_out_result = {
        "slc_release": {
            "path": str(export_release_tar_gz_file),
            "goal": "release",
        },
        "slc_test": {
            "path": str(export_test_tar_gz_file),
            "goal": "base_test_build_run",
        },
    }

    with LocalDockerRegistryContextManager(repository_name) as registry:
        build_repository = registry.name
        release_repository = "dummy/releases"
        build_config_path.write_text(
            build_config_content.format(
                build_repository=build_repository, release_repository=release_repository
            )
        )
        export_and_scan_vulnerabilities(
            build_mode=BuildMode.NORMAL,
            flavor=flavor_name,
            branch_name=branch_name,
            docker_user=docker_user,
            docker_password=docker_password,
            commit_sha=commit_sha,
            github_access=github_access,
        )

        expected_images = {
            "name": repository_name,
            "tags": [
                _build_tag_name_ci("", flavor_name, arch, tag_info)
                for tag_info in EXPECTED_TAG_INFO_HASHES
            ]
            + [
                _build_tag_name_ci(commit_sha, flavor_name, arch, tag_info)
                for tag_info in EXPECTED_TAG_INFO_HASHES
            ],
        }

        assert json.loads(github_access.result) == exported_github_out_result

        assert registry.images["name"] == expected_images["name"]
        assert set(registry.images["tags"]) == set(expected_images["tags"])


def test_cd(flavors_path, tmp_test_dir: str):
    flavor_name = "successful"
    machine = platform.machine().lower()
    arch = "arm64" if ("arm" in machine) or ("aarch" in machine) else "x64"

    branch_name = "test_branch"
    docker_user = None
    docker_password = None

    commit_sha = "123"
    github_access = TestGithubAccess()

    shutil.copytree(src=flavors_path, dst=Path(tmp_test_dir) / "flavors")

    build_config_path = Path(tmp_test_dir) / "build_config.json"
    build_config_content = cleandoc("""
 {{
    "ignore_paths": [
      "some_path"
    ],
    "docker_build_repository": "{build_repository}",
    "docker_release_repository": "{release_repository}",
    "test_container_folder": "test_container"
}}
""")

    repository_name = "test_export_and_scan_vulnerabilities"
    release_hash = [tag_info.tag_suffix for tag_info in EXPECTED_TAG_INFO_HASHES if tag_info.build_step == "release"][0]
    test_hash = [
        tag_info.tag_suffix
        for tag_info in EXPECTED_TAG_INFO_HASHES
        if tag_info.build_step == "base_test_build_run"
    ][0]
    export_release_tar_gz_file = Path(tmp_test_dir) / ".build_output_release" / "cache" / "exports" / f"{flavor_name}-release-{arch}-{release_hash}.tar.gz"
    export_test_tar_gz_file = Path(tmp_test_dir) / ".build_output_test" / "cache" / "exports" / f"{flavor_name}-base_test_build_run-{arch}-{test_hash}.tar.gz"
    exported_github_out_result = {
        "slc_release": {
            "path": str(export_release_tar_gz_file),
            "goal": "release",
        },
        "slc_test": {
            "path": str(export_test_tar_gz_file),
            "goal": "base_test_build_run",
        },
    }

    with LocalDockerRegistryContextManager(repository_name) as registry:
        build_repository = "dummy/build"
        release_repository = registry.name
        build_config_path.write_text(
            build_config_content.format(
                build_repository=build_repository, release_repository=release_repository
            )
        )
        export_and_scan_vulnerabilities(
            build_mode=BuildMode.RELEASE,
            flavor=flavor_name,
            branch_name=branch_name,
            docker_user=docker_user,
            docker_password=docker_password,
            commit_sha=commit_sha,
            github_access=github_access,
        )

        expected_images = {
            "name": repository_name,
            "tags": [
                _build_tag_name_cd(flavor_name, arch, branch_name, tag_info)
                for tag_info in EXPECTED_TAG_INFO_RELEASE
            ]
        }

        assert json.loads(github_access.result) == exported_github_out_result

        assert registry.images["name"] == expected_images["name"]
        assert set(registry.images["tags"]) == set(expected_images["tags"])
