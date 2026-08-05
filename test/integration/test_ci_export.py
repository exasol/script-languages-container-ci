from pathlib import Path
from tempfile import TemporaryDirectory
from test.integration.utils import cleanup_images

import pytest

from exasol.slc_ci.lib.ci_export import CIExport


@pytest.mark.parametrize("goal", ["release", "base_test_build_run"])
@pytest.mark.parametrize("build_name", [None, "test_build_name"])
def test(flavors_path, goal, build_name):
    flavor_name = "successful"
    flavor_path = str(flavors_path / flavor_name)
    with cleanup_images(Path(flavor_path)):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            slc_dir = Path(temp_dir) / "slc"
            res = CIExport().export(
                flavor_path=(flavor_path,),
                goal=goal,
                output_directory=str(output_dir),
                build_name=build_name,
                export_path=str(slc_dir),
                use_symlink_for_export_path=True,
            )
            assert res.exists()
            assert res.name.endswith("tar.gz")
            assert res.name.startswith(flavor_name)
            assert res.parent == slc_dir
            assert res.is_symlink()

            if build_name:
                assert build_name in res.name
