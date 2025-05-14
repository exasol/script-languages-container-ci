from test.asserts import not_raises

import pytest

from exasol.slc_ci.lib.ci_build_test_container import CIBuildTestContainer

testdata = [
    (
        "test_docker_build_repository",
        "test_commit_sha",
        "test_docker_build_repository",
        "test_commit_sha_",
    ),
    (None, "", "exasol/script-language-container", ""),
]


@pytest.mark.parametrize(
    "input_docker_build_repository,input_commit_sha,expected_docker_build_repository,expected_source_tag_prefix",
    testdata,
)
def test(
    input_docker_build_repository,
    input_commit_sha,
    expected_docker_build_repository,
    expected_source_tag_prefix,
    test_containers_folder,
):
    test_type = "successful"
    test_container_folder = str(test_containers_folder / test_type)
    with not_raises(Exception):
        CIBuildTestContainer().build_test_container(
            rebuild=True,
            build_docker_repository=input_docker_build_repository,
            commit_sha=input_commit_sha,
            docker_user=None,
            docker_password=None,
            test_container_folder=test_container_folder,
        )
