from pathlib import Path

import pytest

from exasol.slc_ci.model.build_config_model import BuildConfig
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig, TestConfig, TestSet
from test.unit.github.test_env import test_env


@pytest.fixture
def build_config_environment(tmp_test_dir):
    with open("build_config.json", "w") as f:
        f.write(test_env.build_config.model_dump_json())
    return test_env.build_config


@pytest.fixture
def build_config_with_flavor_environment(
    build_config_environment: BuildConfig
):
    build_config_environment.flavors_path.mkdir(exist_ok=False)
    flavor_path = build_config_environment.flavors_path / test_env.flavor_name
    flavor_path.mkdir(exist_ok=False)

    config_file_path = flavor_path / "ci.json"

    with open(config_file_path, "w") as f:
        ci_config = test_env.flavor_ci_config.model_dump_json()
        f.write(ci_config)
    return build_config_environment
