import contextlib
import dataclasses
import json
import platform
import shutil
from enum import Enum
from inspect import cleandoc
from pathlib import Path
from test.integration.tag_infos import (
    EXPECTED_LOCAL_TAG_INFO_HASHES,
    EXPECTED_LOCAL_TAG_INFO_RELEASE,
    EXPECTED_TAG_INFO_HASHES,
    EXPECTED_TAG_INFO_RELEASE,
    TagInfo,
)

import docker
import pytest
from exasol.slc.api import clean_flavor_images
from exasol_integration_test_docker_environment.testing.docker_registry import (
    LocalDockerRegistryContextManager,
)

from exasol.slc_ci.lib.export_and_scan_vulnerabilities import (
    export_and_scan_vulnerabilities,
)
from exasol.slc_ci.model.build_mode import BuildMode


class GithubAccessMock:
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


def _build_local_tag_name_ci(flavor_name: str, arch: str, tag_info: TagInfo) -> str:
    return f"exasol/script-language-container:{flavor_name}-{tag_info.build_step}_{arch}_{tag_info.tag_suffix}"


def _build_local_tag_name_cd(
    flavor_name: str, arch: str, branch_name: str, tag_info: TagInfo
) -> str:
    return f"exasol/script-language-container:{flavor_name}-{tag_info.build_step}_{arch}_{branch_name}"


class BuildConfigMode(Enum):
    NORMAL = "normal"
    RELEASE = "release"
    MASTER = "master"


@dataclasses.dataclass(frozen=True)
class BuildTestConfig:
    build_cfg_mode: BuildConfigMode
    branch_name: str

    @property
    def build_mode(self) -> BuildMode:
        table = {
            BuildConfigMode.NORMAL: BuildMode.NORMAL,
            BuildConfigMode.RELEASE: BuildMode.RELEASE,
            BuildConfigMode.MASTER: BuildMode.NORMAL,
        }
        return table[self.build_cfg_mode]


def _get_docker_images_for_flavor(flavor: str) -> set[str]:
    docker_client = docker.from_env()
    try:
        exa_images = [
            str(tag)
            for img in docker_client.images.list()
            for tag in img.tags
            if tag.startswith(f"exasol/script-language-container:{flavor}")
        ]
        return set(exa_images)

    finally:
        docker_client.close()


@contextlib.contextmanager
def _cleanup_images(flavor_path: Path):
    clean_flavor_images(
        flavor_path=(str(flavor_path),),
    )
    yield
    clean_flavor_images(
        flavor_path=(str(flavor_path),),
    )


@pytest.mark.parametrize(
    "build_test_config",
    [
        pytest.param(
            BuildTestConfig(
                build_cfg_mode=BuildConfigMode.NORMAL,
                branch_name="refs/heads/some_branch",
            ),
            id="ci-pr",
        ),
        pytest.param(
            BuildTestConfig(
                build_cfg_mode=BuildConfigMode.RELEASE, branch_name="1.2.3"
            ),
            id="cd",
        ),
        pytest.param(
            BuildTestConfig(
                build_cfg_mode=BuildConfigMode.MASTER, branch_name="refs/heads/master"
            ),
            id="ci-master",
        ),
    ],
)
def test_export_and_scan_vulnerabilities(
    flavors_path, tmp_test_dir: str, build_test_config
):
    flavor_name = "successful"
    machine = platform.machine().lower()
    arch = "arm64" if ("arm" in machine) or ("aarch" in machine) else "x64"

    branch_name = build_test_config.branch_name
    build_mode = build_test_config.build_mode
    docker_user = None
    docker_password = None

    commit_sha = "123"
    github_access = GithubAccessMock()

    local_flavors_path = Path(tmp_test_dir) / "flavors"
    shutil.copytree(src=flavors_path, dst=local_flavors_path)

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

    release_hash = [
        tag_info.tag_suffix
        for tag_info in EXPECTED_TAG_INFO_HASHES
        if tag_info.build_step == "release"
    ][0]
    test_hash = [
        tag_info.tag_suffix
        for tag_info in EXPECTED_TAG_INFO_HASHES
        if tag_info.build_step == "base_test_build_run"
    ][0]
    export_release_tar_gz_file = (
        Path(tmp_test_dir)
        / ".build_output_release"
        / "cache"
        / "exports"
        / f"{flavor_name}-release-{arch}-{release_hash}.tar.gz"
    )
    export_test_tar_gz_file = (
        Path(tmp_test_dir)
        / ".build_output_test"
        / "cache"
        / "exports"
        / f"{flavor_name}-base_test_build_run-{arch}-{test_hash}.tar.gz"
    )
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

    repository_name_build = "test_export_and_scan_vulnerabilities_build"
    repository_name_release = "test_export_and_scan_vulnerabilities_release"

    with LocalDockerRegistryContextManager(repository_name_build) as build_registry:
        with LocalDockerRegistryContextManager(
            repository_name_release
        ) as release_registry:
            with _cleanup_images(local_flavors_path / flavor_name):
                if build_test_config.build_cfg_mode == BuildConfigMode.NORMAL:
                    build_repository = build_registry.name
                    release_repository = "dummy/releases"
                    expected_tags_build_registry = [
                        _build_tag_name_ci("", flavor_name, arch, tag_info)
                        for tag_info in EXPECTED_TAG_INFO_HASHES
                    ] + [
                        _build_tag_name_ci(commit_sha, flavor_name, arch, tag_info)
                        for tag_info in EXPECTED_TAG_INFO_HASHES
                    ]
                    expected_tags_release_registry = []
                    expected_local_images = [
                        _build_local_tag_name_ci(flavor_name, arch, tag_info)
                        for tag_info in EXPECTED_LOCAL_TAG_INFO_HASHES
                    ]
                elif build_test_config.build_cfg_mode == BuildConfigMode.RELEASE:
                    build_repository = "dummy/build"
                    release_repository = release_registry.name
                    expected_tags_release_registry = [
                        _build_tag_name_cd(flavor_name, arch, branch_name, tag_info)
                        for tag_info in EXPECTED_TAG_INFO_RELEASE
                    ]
                    expected_tags_build_registry = []
                    expected_local_images = [
                        _build_local_tag_name_cd(
                            flavor_name, arch, branch_name, tag_info
                        )
                        for tag_info in EXPECTED_LOCAL_TAG_INFO_RELEASE
                    ]
                elif build_test_config.build_cfg_mode == BuildConfigMode.MASTER:
                    build_repository = build_registry.name
                    release_repository = release_registry.name
                    expected_tags_build_registry = [
                        _build_tag_name_ci("", flavor_name, arch, tag_info)
                        for tag_info in EXPECTED_TAG_INFO_HASHES
                    ] + [
                        _build_tag_name_ci(commit_sha, flavor_name, arch, tag_info)
                        for tag_info in EXPECTED_TAG_INFO_HASHES
                    ]
                    expected_tags_release_registry = [
                        _build_tag_name_ci("", flavor_name, arch, tag_info)
                        for tag_info in EXPECTED_TAG_INFO_HASHES
                    ]
                    expected_local_images = [
                        _build_local_tag_name_ci(flavor_name, arch, tag_info)
                        for tag_info in EXPECTED_LOCAL_TAG_INFO_HASHES
                    ]

                build_config_path.write_text(
                    build_config_content.format(
                        build_repository=build_repository,
                        release_repository=release_repository,
                    )
                )
                export_and_scan_vulnerabilities(
                    build_mode=build_mode,
                    flavor=flavor_name,
                    branch_name=branch_name,
                    docker_user=docker_user,
                    docker_password=docker_password,
                    commit_sha=commit_sha,
                    github_access=github_access,
                )

                assert json.loads(github_access.result) == exported_github_out_result

                expected_images_build_registry = {
                    "name": repository_name_build,
                    "tags": expected_tags_build_registry,
                }

                expected_images_release_registry = {
                    "name": repository_name_release,
                    "tags": expected_tags_release_registry,
                }

                if expected_tags_build_registry:
                    assert (
                        build_registry.images["name"]
                        == expected_images_build_registry["name"]
                    )
                    assert set(build_registry.images["tags"]) == set(
                        expected_images_build_registry["tags"]
                    )
                else:
                    with pytest.raises(KeyError):
                        images = build_registry.images["name"]

                if expected_tags_release_registry:
                    assert (
                        release_registry.images["name"]
                        == expected_images_release_registry["name"]
                    )
                    assert set(release_registry.images["tags"]) == set(
                        expected_images_release_registry["tags"]
                    )
                else:
                    with pytest.raises(KeyError):
                        images = release_registry.images["name"]

                images = _get_docker_images_for_flavor(flavor_name)
                assert images == set(expected_local_images)
