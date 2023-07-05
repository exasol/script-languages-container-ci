import logging
import os
from pathlib import Path

import pytest

from exasol_script_languages_container_ci.lib.ci_build import CIBuild
from test.asserts import not_raises

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
    test_type = "successful"
    flavor_path = str(flavors_path / test_type)
    test_container_folder = str(test_containers_folder / test_type)
    print("cwd",Path(".").absolute())
    with not_raises(Exception):
        CIBuild().build(
            flavor_path=(flavor_path,),
            rebuild=True,
            commit_sha=input_commit_sha,
            build_docker_repository=input_docker_build_repository,
            docker_user=None,
            docker_password=None,
            test_container_folder=test_container_folder
        )
