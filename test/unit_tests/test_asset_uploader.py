from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union
from unittest.mock import create_autospec, MagicMock

from exasol_script_languages_container_ci.lib.asset_uploader import AssetUploader
from exasol_script_languages_container_ci.lib.github_release_asset_uploader import GithubReleaseAssetUploader
from test.mock_cast import mock_cast


def test():
    github_release_asset_uploader_mock: Union[MagicMock, GithubReleaseAssetUploader] = \
        create_autospec(GithubReleaseAssetUploader)
    asset_uploader = AssetUploader(release_uploader=github_release_asset_uploader_mock)
    with TemporaryDirectory() as temp_dir:
        artifact_path = Path(temp_dir)
        release_artifact = artifact_path / "test_artifact.txt"
        with open(release_artifact, "w") as f:
            f.write("test")
        asset_uploader.upload_assets(
            repo_id="test_repo_id",
            release_id=123,
            file_suffix=".txt",
            content_type="test_content_type",
            label_prefix="test_label_prefix",
            artifact_path=temp_dir
        )
        mock_cast(github_release_asset_uploader_mock.upload).assert_called_once_with(
            archive_path=str(release_artifact),
            content_type='test_content_type',
            label='test_label_prefix test_artifact',
            release_id=123,
            repo_id='test_repo_id'
        )
