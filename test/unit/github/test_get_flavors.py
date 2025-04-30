import json
from unittest.mock import MagicMock

from exasol.slc_ci.lib.get_flavors import get_flavors as lib_get_flavors

def test_get_flavors(build_config_environment):

    github_output_mock = MagicMock()
    build_config_environment.flavors_path.mkdir(exist_ok=False)
    (build_config_environment.flavors_path / "flavor_a").mkdir(exist_ok=False)

    (build_config_environment.flavors_path / "flavor_b").mkdir(exist_ok=False)

    lib_get_flavors(github_access=github_output_mock)
    res = github_output_mock.write_result.call_args.args[0]
    res = set(json.loads(res))
    assert res == {"flavor_a", "flavor_b"}

def test_get_flavors_ignore_files(build_config_environment):
    github_output_mock = MagicMock()
    build_config_environment.flavors_path.mkdir(exist_ok=False)
    (build_config_environment.flavors_path / "flavor_a").mkdir(exist_ok=False)

    (build_config_environment.flavors_path / "flavor_b").mkdir(exist_ok=False)

    with open(build_config_environment.flavors_path / "some_file.txt", "w") as f:
        f.write("some content")

    lib_get_flavors(github_access=github_output_mock)
    res = github_output_mock.write_result.call_args.args[0]
    res = set(json.loads(res))
    assert res == {"flavor_a", "flavor_b"}
