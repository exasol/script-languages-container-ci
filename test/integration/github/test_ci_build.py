from test.asserts import not_raises

import pytest

from exasol.slc_ci.lib.ci_build import CIBuild

testdata = [
    (
        "test_docker_build_repository",
        "test_docker_build_repository",
    ),
    (None, "exasol/script-language-container"),
]


@pytest.mark.parametrize(
    "input_docker_build_repository,expected_docker_build_repository",
    testdata,
)
def test(
    input_docker_build_repository,
    expected_docker_build_repository,
    flavors_path,
):
    test_type = "successful"
    flavor_path = str(flavors_path / test_type)
    with not_raises(Exception):
        CIBuild().build(
            flavor_path=(flavor_path,),
            rebuild=True,
            build_docker_repository=input_docker_build_repository,
            docker_user=None,
            docker_password=None,
        )
