from pathlib import Path
from tempfile import TemporaryDirectory

from exasol_script_languages_container_ci.lib.ci_export import CIExport


def test():
    script_path = Path(__file__).absolute().parent
    resources_path = script_path / "resources"
    flavor_path = str(resources_path / "flavors" / "real-test-flavor")
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
