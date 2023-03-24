from pathlib import Path
from tempfile import TemporaryDirectory

from exasol_integration_test_docker_environment.lib.docker.images.image_info import ImageState

from exasol_script_languages_container_ci.lib.ci_build import CIBuild
from exasol_script_languages_container_ci.lib.ci_export import CIExport
from test.conftest import DockerConfig


def test():
    script_path = Path(__file__).absolute().parent
    flavor_path = str(script_path / "flavors" / "real-test-flavor")
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