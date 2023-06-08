from pathlib import Path

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
         test_container_folder):
    flavor_name = "functioning"
    flavor_path = str(flavors_path / flavor_name)
    slc_image_infos, test_container_image_infos = \
        CIBuild().build(
            flavor_path=(flavor_path,),
            rebuild=True,
            commit_sha=input_commit_sha,
            build_docker_repository=input_docker_build_repository,
            docker_user=None,
            docker_password=None,
            test_container_folder=str(test_container_folder)
        )
    expected_images = {'release', 'base_test_build_run', 'flavor_test_build_run'}
    actual_images = {key for key in slc_image_infos[flavor_path]}
    assert flavor_path in slc_image_infos.keys() \
           and expected_images == actual_images \
           and slc_image_infos[flavor_path]["release"].target_tag == f"{flavor_name}-release" \
           and slc_image_infos[flavor_path]["release"].target_repository_name == 'exasol/script-language-container' \
           and slc_image_infos[flavor_path][
               "release"].source_tag == f"{expected_source_tag_prefix}{flavor_name}-release" \
           and slc_image_infos[flavor_path]["release"].source_repository_name == expected_docker_build_repository \
           and slc_image_infos[flavor_path]["release"].image_state == ImageState.WAS_BUILD.name \
           and test_container_image_infos.target_tag == "db-test-container" \
           and test_container_image_infos.target_repository_name == 'exasol/script-language-container' \
           and test_container_image_infos.source_tag == f"{expected_source_tag_prefix}db-test-container" \
           and test_container_image_infos.source_repository_name == expected_docker_build_repository
