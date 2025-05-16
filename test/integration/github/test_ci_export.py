from tempfile import TemporaryDirectory

import pytest

from exasol.slc_ci.lib.ci_export import CIExport


@pytest.mark.parametrize("goal", ["release", "base_test_build_run"])
def test(flavors_path, goal):
    flavor_name = "successful"
    flavor_path = str(flavors_path / flavor_name)
    with TemporaryDirectory() as temp_dir:
        res = CIExport().export(
            flavor_path=(flavor_path,), goal=goal, output_directory=temp_dir
        )
        assert res.exists()
        assert res.name.endswith("tar.gz")
        assert res.name.startswith(flavor_name)
