from pathlib import Path
from tempfile import TemporaryDirectory

from exasol_script_languages_container_ci.lib.ci_export import CIExport


def test(flavors_path):
    flavor_name = "successful"
    flavor_path = str(flavors_path / flavor_name)
    with TemporaryDirectory() as temp_dir:
        CIExport().export(flavor_path=(flavor_path,), export_path=temp_dir)
        temp_dir_path = Path(temp_dir)
        temp_dir_content = set(temp_dir_path.iterdir())
        files_start_with_flavor_name = [str(file.name).startswith(flavor_name) for file in temp_dir_content]
        assert len(temp_dir_content) == 2 and all(files_start_with_flavor_name)
