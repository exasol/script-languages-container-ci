import dataclasses
import platform

import pytest
from exasol_integration_test_docker_environment.testing.docker_registry import (
    LocalDockerRegistryContextManager,
)

from exasol.slc_ci.lib.ci_push import CIPush
from test.integration.tag_infos import (
    EXPECTED_TAG_INFO_HASHES,
    TagInfo,
    EXPECTED_TAG_INFO_RELEASE,
)


def build_tag_name(flavor_name: str, arch: str, tag_info: TagInfo) -> str:
    return f"tag_{flavor_name}-{tag_info.build_step}_{arch}_{tag_info.tag_suffix}"


@dataclasses.dataclass(frozen=True)
class _CiTestConfig:
    expected_tag_infos: list[TagInfo]
    build_name: str | None


@pytest.mark.parametrize(
    "test_ci_config",
    [
        _CiTestConfig(
            expected_tag_infos=EXPECTED_TAG_INFO_RELEASE, build_name="test-build_1.2.3"
        ),
        _CiTestConfig(expected_tag_infos=EXPECTED_TAG_INFO_HASHES, build_name=None),
    ],
)
def test(flavors_path, test_ci_config):
    flavor_name = "successful"
    flavor_path = str(flavors_path / flavor_name)
    machine = platform.machine().lower()
    arch = "arm64" if ("arm" in machine) or ("aarch" in machine) else "x64"

    with LocalDockerRegistryContextManager("test_ci_push") as registry:
        CIPush().push(
            flavor_path=(flavor_path,),
            target_docker_repository=registry.name,
            target_docker_tag_prefix="tag",
            docker_user=None,
            docker_password=None,
            build_name=test_ci_config.build_name,
        )

        expected_images = {
            "name": "test_ci_push",
            "tags": [
                build_tag_name(flavor_name, arch, tag_info)
                for tag_info in test_ci_config.expected_tag_infos
            ],
        }

        assert expected_images["name"] == registry.images["name"]
        assert set(expected_images["tags"]) == set(registry.images["tags"])
