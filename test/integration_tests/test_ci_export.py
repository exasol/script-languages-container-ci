from pathlib import Path
from tempfile import TemporaryDirectory

from exasol_script_languages_container_ci.lib.ci_export import CIExport


def test(flavors_path):
    flavor_name = "functioning"
    flavor_path = str(flavors_path / flavor_name)
    with TemporaryDirectory() as temp_dir:
        export_result = CIExport().export(flavor_path=(flavor_path,), export_path=temp_dir)
        temp_dir_content = set(Path(temp_dir).iterdir())
        assert \
            flavor_path in export_result.export_infos \
            and "release" in export_result.export_infos[flavor_path] \
            and Path(export_result.export_infos[flavor_path]["release"].output_file).parent == Path(temp_dir) \
            and Path(export_result.export_infos[flavor_path]["release"].output_file) in temp_dir_content \
            and Path(
                export_result.export_infos[flavor_path]["release"].output_file + ".sha512sum") in temp_dir_content
