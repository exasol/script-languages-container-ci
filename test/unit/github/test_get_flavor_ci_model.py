import pytest
from pydantic import ValidationError

import exasol.slc_ci.lib.get_flavor_ci_model as lib_get_flavor_ci_model
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig, TestConfig, TestSet


def test_get_flavor_ci_model(build_config_environment):
    build_config_environment.flavors_path.mkdir(exist_ok=False)
    flavor_path = build_config_environment.flavors_path / "flavor_a"
    flavor_path.mkdir(exist_ok=False)

    config_file_path = flavor_path / "ci.json"

    with open(config_file_path, "w") as f:
        ci_config = """
        {
          "build_runner": "ubuntu-22.04",
          "test_config": {
            "test_runner": "ubuntu-22.04",
            "test_sets": [
              {
                "name": "all",
                "folders": ["python3/all"]
              },
              {
                "name": "pandas",
                "folders": ["pandas/all", "pandas/pandas2"]
              }
            ]
          }
        }
        """
        f.write(ci_config)
    res = lib_get_flavor_ci_model.get_flavor_ci_model(build_config_environment, "flavor_a")
    assert res == FlavorCiConfig(
        build_runner="ubuntu-22.04",
        test_config=TestConfig(
            test_runner="ubuntu-22.04",
            test_sets=[
                TestSet(name="all", folders=["python3/all"]),
                TestSet(name="pandas", folders=["pandas/all", "pandas/pandas2"]),
            ],
        ),
    )


def test_get_flavor_ci_model_fails_with_wrong_json(build_config_environment):
    build_config_environment.flavors_path.mkdir(exist_ok=False)
    flavor_path = build_config_environment.flavors_path / "flavor_a"
    flavor_path.mkdir(exist_ok=False)

    config_file_path = flavor_path / "ci.json"

    with open(config_file_path, "w") as f:
        ci_config = """
        {
          "______________build_runners_______": "ubuntu-22.04",
          "test_config": {
            "test_runner": "ubuntu-22.04",
            "test_sets": [
              {
                "name": "all",
                "folders": ["python3/all"]
              },
              {
                "name": "pandas",
                "folders": ["pandas/all", "pandas/pandas2"]
              }
            ]
          }
        }
        """
        f.write(ci_config)
    with pytest.raises(ValidationError):
        lib_get_flavor_ci_model.get_flavor_ci_model(build_config_environment, "flavor_a")
