from exasol.slc_ci.model.build_config import BuildConfig
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig, TestConfig, TestSet
from test.unit.github.test_env import test_env
import exasol.slc_ci.lib.get_flavor_ci_model as lib_get_flavor_ci_model

def test_get_flavor_ci_model(tmp_path):
    base_build_config = test_env.build_config
    build_config = BuildConfig(root=tmp_path, base_branch=base_build_config.base_branch, ignore_paths=base_build_config.ignore_paths,
                               docker_build_repository=base_build_config.docker_build_repository, docker_release_repository=base_build_config.docker_release_repository,
                               test_container_folder=base_build_config.test_container_folder)
    build_config.flavors_path.mkdir(exist_ok=False)
    flavor_path = build_config.flavors_path / "flavor_a"
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
    res = lib_get_flavor_ci_model.get_flavor_ci_model(build_config, "flavor_a")
    assert res == FlavorCiConfig(build_runner="ubuntu-22.04",test_config= TestConfig(test_runner="ubuntu-22.04",test_sets=[TestSet(name="all", folders=["python3/all"]), TestSet(name="pandas", folders=["pandas/all", "pandas/pandas2"])]))



