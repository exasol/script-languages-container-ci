from pathlib import Path

from exasol_integration_test_docker_environment.testing.docker_registry import LocalDockerRegistryContextManager

from exasol_script_languages_container_ci.lib.ci_push import CIPush
from test.conftest import DockerConfig


def test():
    script_path = Path(__file__).absolute().parent
    flavor_path = str(script_path / "flavors" / "real-test-flavor")
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
                 'tag_real-test-flavor-base_test_build_run_PIZOHDCUUA5C4QZEK4FGI2JA2BEYBFFC4E5FJNHW6PPD3HYQSTRA',
                 'tag_real-test-flavor-release_GZMZ7BEX4Y6MBG5ZWLQQEFJIKXK6UCTJFJGABSOLIFQ7FHJIRNVA',
                 'tag_real-test-flavor-flavor_test_build_run_YXYWVE3QGQ6OMNEBJ6T5Z7RMYOR3O3BJVR2DKPR5LBA64MDBKPQA'
             ]}
        assert expected_images == registry.images
