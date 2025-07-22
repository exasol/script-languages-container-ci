from pathlib import Path

from exasol.slc.models.accelerator import Accelerator

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
            default_test_runner="some_test_runner",
            test_sets=[
                TestSet(
                    name="all",
                    files=[],
                    folders=["python3/all/fast"],
                    goal="release",
                    generic_language_tests=[],
                ),
                TestSet(
                    name="pandas",
                    files=["python3/pandas/slow/emit_dtypes_memory_leak.py"],
                    folders=[],
                    goal="release",
                    generic_language_tests=[],
                ),
                TestSet(
                    name="pandas",
                    files=["python3/pandas/slow/dataframe_memory_leak.py"],
                    folders=[],
                    goal="release",
                    generic_language_tests=[],
                ),
                TestSet(
                    name="pandas",
                    files=[],
                    folders=["python3/pandas"],
                    goal="release",
                    generic_language_tests=[],
                ),
                TestSet(
                    name="generic",
                    files=[],
                    folders=[],
                    goal="release",
                    generic_language_tests=["python3"],
                ),
                TestSet(
                    name="gpu",
                    files=[],
                    folders=["gpu"],
                    goal="release",
                    generic_language_tests=[],
                    test_runner="gpu_runner",
                    accelerator=Accelerator.NVIDA,
                ),
            ],
        ),
    )

    flavor_name = "flavor_a"


test_env = TestEnv()
