from pathlib import Path

from exasol.slc_ci.model.build_config_model import BuildConfig
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig, TestConfig, TestSet


class TestEnv:
    docker_user = "test_docker_user"
    docker_pwd = "test_docker_pwd"
    commit_sha = "test_commit_sha"
    branch_name = "test_branch_name"

    build_config = BuildConfig(
        ignore_paths=[Path("doc"), Path("githooks")],
        docker_build_repository="test/script-languages-build-cache",
        docker_release_repository="test/script-language-container",
        test_container_folder="test_container",
    )

    flavor_ci_config = FlavorCiConfig(
        build_runner="some_runner",
        test_config=TestConfig(
            test_runner="some_test_runner",
            test_sets=[
                TestSet(
                    name="all", folders=["python3/all"], test_languages=["python3"], goal="release",
                ),
                TestSet(
                    name="pandas",
                    folders=["python3/pandas"],
                    test_languages=["python3"],
                    goal="release",
                ),
            ],
        ),
    )

    flavor_name = "flavor_a"


test_env = TestEnv()
