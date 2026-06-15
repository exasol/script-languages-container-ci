import dataclasses
import platform

import pytest
from exasol_integration_test_docker_environment.testing.docker_registry import (
    LocalDockerRegistryContextManager,
)

from exasol.slc_ci.lib.ci_push import CIPush


@dataclasses.dataclass(frozen=True)
class _CiTestTagInfo:
    tag_suffix: str
    build_step: str

    def build_tag_name(self, flavor_name: str, arch: str) -> str:
        return f"tag_{flavor_name}-{self.build_step}_{arch}_{self.tag_suffix}"


@dataclasses.dataclass(frozen=True)
class _CiTestConfig:
    expected_tag_infos: list[_CiTestTagInfo]
    build_name: str | None


EXPECTED_TAG_INFO_HASHES = [
    _CiTestTagInfo(
        build_step="base_test_build_run",
        tag_suffix="GUA7R5J3UM27WOHJSQPX2OJNSIEKWCM5YF5GJXKKXZI53LZPV75Q",
    ),
    _CiTestTagInfo(
        build_step="flavor_test_build_run",
        tag_suffix="G2OIMXJ2S3VS2EUAQNW4KWQLX3B2C27XYZ2SDMF7TQRS3UMAUWJQ",
    ),
    _CiTestTagInfo(
        build_step="release",
        tag_suffix="MNWZZGSSFQ6VCLBDH7CZBEZC4K35QQBSLOW5DSYHF3DFFDX2OOZQ",
    ),
]

BUILD_NAME = "test-build_1.2.3"

EXPECTED_TAG_INFO_RELEASE = [
    _CiTestTagInfo(build_step="base_test_build_run", tag_suffix=BUILD_NAME),
    _CiTestTagInfo(build_step="flavor_test_build_run", tag_suffix=BUILD_NAME),
    _CiTestTagInfo(build_step="release", tag_suffix=BUILD_NAME),
]


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
                tag_info.build_tag_name(flavor_name, arch)
                for tag_info in test_ci_config.expected_tag_infos
            ],
        }

        assert expected_images["name"] == registry.images["name"]
        assert set(expected_images["tags"]) == set(registry.images["tags"])
