from pathlib import Path

import pytest

from exasol.slc_ci.model.build_config_model import BuildConfig
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig, TestConfig, TestSet


@pytest.fixture
def build_config():
    return BuildConfig(
        ignore_paths=[Path("doc"), Path("githooks")],
        docker_build_repository="test/script-languages-build-cache",
        docker_release_repository="test/script-language-container",
        test_container_folder="test_container",
    )


@pytest.fixture
def build_config_environment(tmp_test_dir, build_config):
    with open("build_config.json", "w") as f:
        f.write(build_config.model_dump_json())
    return build_config


@pytest.fixture
def test_flavor_config():
    return FlavorCiConfig(
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

@pytest.fixture
def flavor_name():
    return "flavor_a"


@pytest.fixture
def build_config_with_flavor_environment(
    build_config_environment: BuildConfig, test_flavor_config, flavor_name
):
    build_config_environment.flavors_path.mkdir(exist_ok=False)
    flavor_path = build_config_environment.flavors_path / flavor_name
    flavor_path.mkdir(exist_ok=False)

    config_file_path = flavor_path / "ci.json"

    with open(config_file_path, "w") as f:
        ci_config = test_flavor_config.model_dump_json()
        f.write(ci_config)
    return build_config_environment
