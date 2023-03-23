from pathlib import Path

from exasol_integration_test_docker_environment.lib.docker.images.image_info import ImageState

from exasol_script_languages_container_ci.lib.ci_build import CIBuild
from test.conftest import DockerConfig


def test():
    script_path = Path(__file__).absolute().parent
    flavor_path = str(script_path / "flavors" / "real-test-flavor")
    test_container_folder = str(script_path / "test_container")
    commit_sha = "commit_sha"
    docker_build_repository = "docker_build_repository"
    slc_image_infos, test_container_image_infos = \
        CIBuild().build(
            flavor_path=(flavor_path,),
            rebuild=True,
            commit_sha=commit_sha,
            build_docker_repository=docker_build_repository,
            docker_user=None,
            docker_password=None,
            test_container_folder=test_container_folder
        )
    expected_images = {'release', 'base_test_build_run', 'flavor_test_build_run'}
    actual_images = {key for key in slc_image_infos[flavor_path]}
    assert flavor_path in slc_image_infos.keys() \
           and expected_images == actual_images \
           and slc_image_infos[flavor_path]["release"].target_tag == "real-test-flavor-release" \
           and slc_image_infos[flavor_path]["release"].target_repository_name == 'exasol/script-language-container' \
           and slc_image_infos[flavor_path]["release"].source_tag == f"{commit_sha}_real-test-flavor-release" \
           and slc_image_infos[flavor_path]["release"].source_repository_name == docker_build_repository \
           and slc_image_infos[flavor_path]["release"].image_state == ImageState.WAS_BUILD.name \
           and test_container_image_infos.target_tag == "db-test-container" \
           and test_container_image_infos.target_repository_name == 'exasol/script-language-container' \
           and test_container_image_infos.source_tag == f"{commit_sha}_db-test-container" \
           and test_container_image_infos.source_repository_name == docker_build_repository
