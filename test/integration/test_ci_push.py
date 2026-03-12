import platform

from exasol_integration_test_docker_environment.testing.docker_registry import (
    LocalDockerRegistryContextManager,
)

from exasol.slc_ci.lib.ci_prepare import get_commit_sha_for_docker_tag
from exasol.slc_ci.lib.ci_push import CIPush


def test(flavors_path):
    flavor_name = "successful"
    flavor_path = str(flavors_path / flavor_name)
    machine = platform.machine().lower()
    arch = "arm64" if ("arm" in machine) or ("aarch" in machine) else "x64"

    with LocalDockerRegistryContextManager("test_ci_push") as registry:
        CIPush().push(
            flavor_path=(flavor_path,),
            target_docker_repository=registry.name,
            target_docker_tag_prefix=get_commit_sha_for_docker_tag("tag"),
            docker_user=None,
            docker_password=None,
        )

        expected_images = {
            "name": "test_ci_push",
            "tags": [
                f"tag_{flavor_name}-base_test_build_run_{arch}_GUA7R5J3UM27WOHJSQPX2OJNSIEKWCM5YF5GJXKKXZI53LZPV75Q",
                f"tag_{flavor_name}-flavor_test_build_run_{arch}_G2OIMXJ2S3VS2EUAQNW4KWQLX3B2C27XYZ2SDMF7TQRS3UMAUWJQ",
                f"tag_{flavor_name}-release_{arch}_MNWZZGSSFQ6VCLBDH7CZBEZC4K35QQBSLOW5DSYHF3DFFDX2OOZQ",
            ],
        }

        assert expected_images["name"] == registry.images["name"]
        assert set(expected_images["tags"]) == set(registry.images["tags"])
