import json

from exasol.slc_ci.lib.get_flavors import get_flavors as lib_get_flavors

def test_get_flavors(build_config_environment, github_output_reader):

    build_config_environment.flavors_path.mkdir(exist_ok=False)
    (build_config_environment.flavors_path / "flavor_a").mkdir(exist_ok=False)

    (build_config_environment.flavors_path / "flavor_b").mkdir(exist_ok=False)

    lib_get_flavors(github_var="flavors")
    res = set(json.loads(github_output_reader(github_var="flavors")))
    assert res == {"flavor_a", "flavor_b"}

def test_get_flavors_ignore_files(build_config_environment, github_output_reader):

    build_config_environment.flavors_path.mkdir(exist_ok=False)
    (build_config_environment.flavors_path / "flavor_a").mkdir(exist_ok=False)

    (build_config_environment.flavors_path / "flavor_b").mkdir(exist_ok=False)

    with open(build_config_environment.flavors_path / "some_file.txt", "w") as f:
        f.write("some content")

    lib_get_flavors(github_var="flavors")
    res = set(json.loads(github_output_reader(github_var="flavors")))
    assert res == {"flavor_a", "flavor_b"}