from pathlib import Path
from tempfile import TemporaryDirectory

from exasol.slc_ci.lib.ci_export import CIExport


def test(flavors_path):
    flavor_name = "successful"
    flavor_path = str(flavors_path / flavor_name)
    with TemporaryDirectory() as temp_dir:
        res = CIExport().export(flavor_path=(flavor_path,), output_directory=temp_dir)
        assert res.exists()
        assert res.name.endswith("tar.gz")
        assert res.name.startswith(flavor_name)
