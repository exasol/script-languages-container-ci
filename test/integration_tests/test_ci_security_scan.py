from pathlib import Path

from exasol_integration_test_docker_environment.lib.docker.images.image_info import ImageState

from exasol_script_languages_container_ci.lib.ci_security_scan import CISecurityScan
from test.conftest import DockerConfig


def test():
    script_path = Path(__file__).absolute().parent
    flavor_path = str(script_path / "flavors" / "real-test-flavor")
    security_scan_result = \
        CISecurityScan().run_security_scan(
            flavor_path=(flavor_path,),
        )
    assert flavor_path in security_scan_result.scan_results_per_flavor \
           and security_scan_result.scan_results_per_flavor[flavor_path].is_ok
