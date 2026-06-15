import dataclasses
import platform

import pytest
from exasol_integration_test_docker_environment.testing.docker_registry import (
    LocalDockerRegistryContextManager,
)

from exasol.slc_ci.lib.ci_push import CIPush

@dataclasses.dataclass(frozen=True)
class _CiTestConfig:
    expected_tag_suffixes: list[str]
    build_name: str | None

EXPECTED_TAG_HASHES = [
                f"GUA7R5J3UM27WOHJSQPX2OJNSIEKWCM5YF5GJXKKXZI53LZPV75Q",
                f"G2OIMXJ2S3VS2EUAQNW4KWQLX3B2C27XYZ2SDMF7TQRS3UMAUWJQ",
                f"MNWZZGSSFQ6VCLBDH7CZBEZC4K35QQBSLOW5DSYHF3DFFDX2OOZQ",
            ]

@pytest.mark.parametrize("test_ci_config", [_CiTestConfig(expected_tag_suffixes=["test-build_1.2.3"]*3, build_name="test-build_1.2.3"),
                                            _CiTestConfig(expected_tag_suffixes=EXPECTED_TAG_HASHES, build_name=None),])
def test(flavors_path, test_ci_config):
    flavor_name = "successful"
    flavor_path = str(flavors_path / flavor_name)
    machine = platform.machine().lower()
    arch = "arm64" if ("arm" in machine) or ("aarch" in machine) else "x64"
    build_name = test_ci_config.build_name

    with LocalDockerRegistryContextManager("test_ci_push") as registry:
        CIPush().push(
            flavor_path=(flavor_path,),
            target_docker_repository=registry.name,
            target_docker_tag_prefix="tag",
            docker_user=None,
            docker_password=None,
            build_name=build_name,
        )

        expected_images = {
            "name": "test_ci_push",
            "tags": [f"tag_{flavor_name}-base_test_build_run_{arch}_{suffix}" for suffix in test_ci_config.expected_tag_suffixes]
        }

        assert expected_images["name"] == registry.images["name"]
        assert set(expected_images["tags"]) == set(registry.images["tags"])
