import pytest
from exasol_integration_test_docker_environment.lib.docker.images.image_info import ImageState

from exasol_script_languages_container_ci.lib.ci_build import CIBuild

testdata = [
    ("test_docker_build_repository", "test_commit_sha", "test_docker_build_repository", "test_commit_sha_"),
    (None, "", "exasol/script-language-container", "")
]


@pytest.mark.parametrize(
    "input_docker_build_repository,input_commit_sha,expected_docker_build_repository,expected_source_tag_prefix",
    testdata)
def test(input_docker_build_repository,
         input_commit_sha,
         expected_docker_build_repository,
         expected_source_tag_prefix,
         flavors_path,
         test_containers_folder):
    flavor_name = "successful_ci_process"
    flavor_path = str(flavors_path / flavor_name)
    test_container_folder = str(test_containers_folder / "successful_test")
    CIBuild().build(
        flavor_path=(flavor_path,),
        rebuild=True,
        commit_sha=input_commit_sha,
        build_docker_repository=input_docker_build_repository,
        docker_user=None,
        docker_password=None,
        test_container_folder=test_container_folder
    )
