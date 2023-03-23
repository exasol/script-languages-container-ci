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
                 'tag_real-test-flavor-flavor_customization_F45XZXWQCCMELESCITR3JMMC3JE37ZEFFYPTOOPACA5K5GQZQVPA',
                 'tag_real-test-flavor-build_run_MSE7AKQDPWTIY57I5EZFHTV7AUCFA73AMBKTOTQOIJ5QTME7G5TQ',
                 'tag_real-test-flavor-flavor_base_deps_YYTQBLTUSMCAHX66BPCRPV3F55N2DJ5XMXJE76OOZQMEVHSX7V3Q',
                 'tag_real-test-flavor-flavor_test_build_run_OK3NFTUGN2G7AWJ4AGMGSWF7GRO7R6Q7FU6JP5OEJKVJGLFKOFBA',
                 'tag_real-test-flavor-udfclient_deps_ELUO3TAV3KYHRCSGN4YT4IMER7LV3HQTSO4ZMDNR4T725P6A4SUA',
                 'tag_real-test-flavor-base_test_deps_Z4WTXVJ364UAL2YHE2267IWI5UOERU2RIZVPSSZVFWWLUDHLWZHQ',
                 'tag_real-test-flavor-language_deps_RDBWIWHW6JUOB3S7GG4ESDJ4A4JEZIXFPU6EQ2N7TOMZIYTLGVDA',
                 'tag_real-test-flavor-build_deps_A3OQAS323XOLGOOLP5KCGBKDXGNXHWXHAGN7ZHAGWVCSHWGLOSVQ',
                 'tag_real-test-flavor-release_RYXKGPEDIIMN4THEZGZYXN6NG44YN6TJB5ZR5QQAQE3TCGTTYNIQ',
                 'tag_real-test-flavor-base_test_build_run_RGIKPN57T7IAVLF2MCDEBWL7GPW4ZA473G2WTDA5Z62JQJHMJODA']}
        assert expected_images == registry.images
