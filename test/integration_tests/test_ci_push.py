from pathlib import Path

from exasol_integration_test_docker_environment.testing.docker_registry import LocalDockerRegistryContextManager

from exasol_script_languages_container_ci.lib.ci_push import CIPush


def test():
    script_path = Path(__file__).absolute().parent
    resources_path = script_path / "resources"
    flavor_path = str(resources_path / "flavors" / "functioning")
    with LocalDockerRegistryContextManager("test_ci_push") as registry:
        CIPush().push(
            flavor_path=(flavor_path,),
            target_docker_repository=registry.name,
            target_docker_tag_prefix="tag",
            docker_user=None,
            docker_password=None
        )
        expected_images = \
            {'name': 'test_ci_push',
             'tags': [
                 'tag_real-test-flavor-base_test_build_run_GUA7R5J3UM27WOHJSQPX2OJNSIEKWCM5YF5GJXKKXZI53LZPV75Q',
                 'tag_real-test-flavor-flavor_test_build_run_G2OIMXJ2S3VS2EUAQNW4KWQLX3B2C27XYZ2SDMF7TQRS3UMAUWJQ',
                 'tag_real-test-flavor-release_MNWZZGSSFQ6VCLBDH7CZBEZC4K35QQBSLOW5DSYHF3DFFDX2OOZQ',
             ]}
        assert expected_images["name"] == registry.images["name"] \
               and set(expected_images["tags"]) == set(registry.images["tags"])
