import contextlib
import dataclasses
import json
import platform
import shutil
from enum import Enum
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
    LocalDockerRegistry,
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


BUILD_REGISTRY_NAME = "test_export_and_scan_vulnerabilities_build"
RELEASE_REGISTRY_NAME = "test_export_and_scan_vulnerabilities_release"


class RepositoryTarget(Enum):
    BUILD_REGISTRY = "build_registry"
    RELEASE_REGISTRY = "release_registry"
    DUMMY_BUILD = "dummy/build"
    DUMMY_RELEASE = "dummy/releases"


class RegistryTagSet(Enum):
    EMPTY = "empty"
    CI_BUILD = "ci_build"
    CI_RELEASE = "ci_release"
    CD_RELEASE = "cd_release"


class LocalImageSet(Enum):
    CI = "ci"
    CD = "cd"


@dataclasses.dataclass(frozen=True)
class RegistryTestConfigTemplate:
    repository_target: RepositoryTarget
    expected_name: str | None
    expected_tags: RegistryTagSet


@dataclasses.dataclass(frozen=True)
class BuildTestConfigTemplate:
    build_mode: BuildMode
    branch_name: str
    build_registry: RegistryTestConfigTemplate
    release_registry: RegistryTestConfigTemplate
    expected_local_images: LocalImageSet


@dataclasses.dataclass(frozen=True)
class BuildTestConfig:
    build_mode: BuildMode
    branch_name: str
    build_repository: str
    release_repository: str
    expected_build_registry: "ExpectedRegistryImages"
    expected_release_registry: "ExpectedRegistryImages"
    expected_local_images: list[str]


@dataclasses.dataclass(frozen=True)
class ExpectedRegistryImages:
    name: str | None
    tags: list[str]


def _expected_registry_tags(
    tag_set: RegistryTagSet,
    flavor_name: str,
    arch: str,
    commit_sha: str,
    branch_name: str,
) -> list[str]:
    match tag_set:
        case RegistryTagSet.EMPTY:
            return []
        case RegistryTagSet.CI_BUILD:
            return [
                _build_tag_name_ci("", flavor_name, arch, tag_info)
                for tag_info in EXPECTED_TAG_INFO_HASHES
            ] + [
                _build_tag_name_ci(commit_sha, flavor_name, arch, tag_info)
                for tag_info in EXPECTED_TAG_INFO_HASHES
            ]
        case RegistryTagSet.CI_RELEASE:
            return [
                _build_tag_name_ci("", flavor_name, arch, tag_info)
                for tag_info in EXPECTED_TAG_INFO_HASHES
            ]
        case RegistryTagSet.CD_RELEASE:
            return [
                _build_tag_name_cd(flavor_name, arch, branch_name, tag_info)
                for tag_info in EXPECTED_TAG_INFO_RELEASE
            ]


def _expected_local_images(
    image_set: LocalImageSet,
    flavor_name: str,
    arch: str,
    branch_name: str,
) -> list[str]:
    match image_set:
        case LocalImageSet.CI:
            return [
                _build_local_tag_name_ci(flavor_name, arch, tag_info)
                for tag_info in EXPECTED_LOCAL_TAG_INFO_HASHES
            ]
        case LocalImageSet.CD:
            return [
                _build_local_tag_name_cd(flavor_name, arch, branch_name, tag_info)
                for tag_info in EXPECTED_LOCAL_TAG_INFO_RELEASE
            ]


def _resolve_repository(
    target: RepositoryTarget,
    build_registry: LocalDockerRegistry,
    release_registry: LocalDockerRegistry,
) -> str:
    repositories = {
        RepositoryTarget.BUILD_REGISTRY: build_registry.name,
        RepositoryTarget.RELEASE_REGISTRY: release_registry.name,
        RepositoryTarget.DUMMY_BUILD: RepositoryTarget.DUMMY_BUILD.value,
        RepositoryTarget.DUMMY_RELEASE: RepositoryTarget.DUMMY_RELEASE.value,
    }
    return repositories[target]


def _expected_registry_images(
    template: RegistryTestConfigTemplate,
    flavor_name: str,
    arch: str,
    commit_sha: str,
    branch_name: str,
) -> ExpectedRegistryImages:
    return ExpectedRegistryImages(
        name=template.expected_name,
        tags=_expected_registry_tags(
            template.expected_tags,
            flavor_name,
            arch,
            commit_sha,
            branch_name,
        ),
    )


def _assert_registry_images(registry, expected_images: ExpectedRegistryImages):
    assert registry.images.get("name") == expected_images.name
    assert set(registry.images.get("tags", [])) == set(expected_images.tags)


def _get_docker_images_for_flavor(flavor: str) -> set[str]:
    docker_client = docker.from_env()
    try:
        return {
            tag
            for img in docker_client.images.list()
            for tag in img.tags
            if tag.startswith(f"exasol/script-language-container:{flavor}")
        }

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


def _tag_suffix_for_build_step(build_step: str) -> str:
    return next(
        tag_info.tag_suffix
        for tag_info in EXPECTED_TAG_INFO_HASHES
        if tag_info.build_step == build_step
    )


BUILD_TEST_CONFIGS = [
    pytest.param(
        BuildTestConfigTemplate(
            build_mode=BuildMode.NORMAL,
            branch_name="refs/heads/some_branch",
            build_registry=RegistryTestConfigTemplate(
                repository_target=RepositoryTarget.BUILD_REGISTRY,
                expected_name=BUILD_REGISTRY_NAME,
                expected_tags=RegistryTagSet.CI_BUILD,
            ),
            release_registry=RegistryTestConfigTemplate(
                repository_target=RepositoryTarget.DUMMY_RELEASE,
                expected_name=None,
                expected_tags=RegistryTagSet.EMPTY,
            ),
            expected_local_images=LocalImageSet.CI,
        ),
        id="ci-pr",
    ),
    pytest.param(
        BuildTestConfigTemplate(
            build_mode=BuildMode.RELEASE,
            branch_name="1.2.3",
            build_registry=RegistryTestConfigTemplate(
                repository_target=RepositoryTarget.DUMMY_BUILD,
                expected_name=None,
                expected_tags=RegistryTagSet.EMPTY,
            ),
            release_registry=RegistryTestConfigTemplate(
                repository_target=RepositoryTarget.RELEASE_REGISTRY,
                expected_name=RELEASE_REGISTRY_NAME,
                expected_tags=RegistryTagSet.CD_RELEASE,
            ),
            expected_local_images=LocalImageSet.CD,
        ),
        id="cd",
    ),
    pytest.param(
        BuildTestConfigTemplate(
            build_mode=BuildMode.NORMAL,
            branch_name="refs/heads/master",
            build_registry=RegistryTestConfigTemplate(
                repository_target=RepositoryTarget.BUILD_REGISTRY,
                expected_name=BUILD_REGISTRY_NAME,
                expected_tags=RegistryTagSet.CI_BUILD,
            ),
            release_registry=RegistryTestConfigTemplate(
                repository_target=RepositoryTarget.RELEASE_REGISTRY,
                expected_name=RELEASE_REGISTRY_NAME,
                expected_tags=RegistryTagSet.CI_RELEASE,
            ),
            expected_local_images=LocalImageSet.CI,
        ),
        id="ci-master",
    ),
]


@pytest.fixture
def arch():
    machine = platform.machine().lower()
    return "arm64" if ("arm" in machine) or ("aarch" in machine) else "x64"


@pytest.fixture
def flavor_name():
    return "successful"


@pytest.fixture
def commit_sha():
    return "123"


@pytest.fixture
def exported_github_out_result(tmp_test_dir: str, flavor_name, arch):
    release_hash = _tag_suffix_for_build_step("release")
    test_hash = _tag_suffix_for_build_step("base_test_build_run")
    return {
        "slc_release": {
            "path": str(
                Path(tmp_test_dir)
                / ".build_output_release"
                / "cache"
                / "exports"
                / f"{flavor_name}-release-{arch}-{release_hash}.tar.gz"
            ),
            "goal": "release",
        },
        "slc_test": {
            "path": str(
                Path(tmp_test_dir)
                / ".build_output_test"
                / "cache"
                / "exports"
                / f"{flavor_name}-base_test_build_run-{arch}-{test_hash}.tar.gz"
            ),
            "goal": "base_test_build_run",
        },
    }


@pytest.fixture
def local_build_registry():
    with LocalDockerRegistryContextManager(BUILD_REGISTRY_NAME) as build_registry:
        yield build_registry


@pytest.fixture
def local_release_registry():
    with LocalDockerRegistryContextManager(RELEASE_REGISTRY_NAME) as release_registry:
        yield release_registry


@pytest.fixture(params=BUILD_TEST_CONFIGS)
def build_test_config(
    request,
    flavor_name,
    arch,
    commit_sha,
    local_build_registry,
    local_release_registry,
):
    template = request.param
    branch_name = template.branch_name
    return BuildTestConfig(
        build_mode=template.build_mode,
        branch_name=branch_name,
        build_repository=_resolve_repository(
            template.build_registry.repository_target,
            local_build_registry,
            local_release_registry,
        ),
        release_repository=_resolve_repository(
            template.release_registry.repository_target,
            local_build_registry,
            local_release_registry,
        ),
        expected_build_registry=_expected_registry_images(
            template.build_registry,
            flavor_name,
            arch,
            commit_sha,
            branch_name,
        ),
        expected_release_registry=_expected_registry_images(
            template.release_registry,
            flavor_name,
            arch,
            commit_sha,
            branch_name,
        ),
        expected_local_images=_expected_local_images(
            template.expected_local_images,
            flavor_name,
            arch,
            branch_name,
        ),
    )


def test_export_and_scan_vulnerabilities(
    flavors_path,
    tmp_test_dir: str,
    build_test_config,
    flavor_name,
    commit_sha,
    local_build_registry,
    local_release_registry,
    exported_github_out_result,
):
    github_access = GithubAccessMock()

    local_flavors_path = Path(tmp_test_dir) / "flavors"
    shutil.copytree(src=flavors_path, dst=local_flavors_path)

    build_config_path = Path(tmp_test_dir) / "build_config.json"
    build_config_path.write_text(
        json.dumps(
            {
                "ignore_paths": ["some_path"],
                "docker_build_repository": build_test_config.build_repository,
                "docker_release_repository": build_test_config.release_repository,
                "test_container_folder": "test_container",
            }
        )
    )

    with _cleanup_images(local_flavors_path / flavor_name):
        export_and_scan_vulnerabilities(
            build_mode=build_test_config.build_mode,
            flavor=flavor_name,
            branch_name=build_test_config.branch_name,
            docker_user=None,
            docker_password=None,
            commit_sha=commit_sha,
            github_access=github_access,
        )

        assert json.loads(github_access.result) == exported_github_out_result

        _assert_registry_images(
            local_build_registry,
            build_test_config.expected_build_registry,
        )
        _assert_registry_images(
            local_release_registry,
            build_test_config.expected_release_registry,
        )

        images = _get_docker_images_for_flavor(flavor_name)
        assert images == set(build_test_config.expected_local_images)
