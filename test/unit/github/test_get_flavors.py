import copy

from exasol.slc_ci.model.build_config import BuildConfig
from test.unit.github.test_env import test_env
import exasol.slc_ci.lib.get_flavors as lib_get_flavors

def test_get_flavors(tmp_path):
    base_build_config = test_env.build_config
    build_config = BuildConfig(root=tmp_path, base_branch=base_build_config.base_branch, ignore_paths=base_build_config.ignore_paths,
                               docker_build_repository=base_build_config.docker_build_repository, docker_release_repository=base_build_config.docker_release_repository,
                               test_container_folder=base_build_config.test_container_folder)
    build_config.flavors_path.mkdir(exist_ok=False)
    (build_config.flavors_path / "flavor_a").mkdir(exist_ok=False)
    (build_config.flavors_path / "flavor_b").mkdir(exist_ok=False)
    res = set(lib_get_flavors.get_flavors(build_config))
    assert res == {"flavor_a", "flavor_b"}
