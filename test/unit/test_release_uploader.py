from test.mock_cast import mock_cast
from typing import Union
from unittest.mock import (
    MagicMock,
    Mock,
    call,
    create_autospec,
    patch,
)

from exasol_script_languages_container_ci.lib.asset_uploader import AssetUploader
from exasol_script_languages_container_ci.lib.ci_export import CIExport
from exasol_script_languages_container_ci.lib.release_uploader import ReleaseUploader


@patch(
    "exasol_script_languages_container_ci.lib.release_uploader.TemporaryDirectory",
    autospec=True,
)
def test(temp_dir_mock):
    asset_uploader_mock: Union[MagicMock, AssetUploader] = create_autospec(  # type: ignore
        AssetUploader
    )
    ci_export_mock: Union[MagicMock, CIExport] = create_autospec(CIExport)  # type: ignore
    release_uploader = ReleaseUploader(asset_uploader_mock, ci_export_mock)
    release_uploader.release_upload(
        release_id=123,
        flavor_path=("test_flavor_path",),
        source_repo_url="https://github.com/test_source_repo_url",
    )
    expected_artifact_path = temp_dir_mock().__enter__()
    assert mock_cast(asset_uploader_mock.upload_assets).mock_calls == [
        call(
            repo_id="test_source_repo_url",
            release_id=123,
            content_type="application/gzip",
            artifact_path=expected_artifact_path,
            file_suffix=".tar.gz",
            label_prefix="Flavor",
        ),
        call(
            repo_id="test_source_repo_url",
            release_id=123,
            content_type="text/plain",
            artifact_path=expected_artifact_path,
            file_suffix=".tar.gz.sha512sum",
            label_prefix="Checksum",
        ),
    ] and mock_cast(ci_export_mock.export).mock_calls == [
        call(flavor_path=("test_flavor_path",), export_path=expected_artifact_path)
    ]
