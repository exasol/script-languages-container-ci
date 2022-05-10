import logging
import glob
import re
from pathlib import Path

from tempfile import TemporaryDirectory
from typing import Tuple, Iterable

import click
from exasol_script_languages_container_tool.cli.commands import export

from exasol_script_languages_container_ci.lib.github_release_asset_uploader import GithubReleaseAssetUploader


def _parse_repo_url(source_repo_url: str) -> str:
    """
    source_repo_url is expected to have the following format: `https://github.com/exasol/script-languages-repo`
    where `exasol/script-languages-repo` is the repository for which the release will be created.
    This method returns the repository id.
    """
    res = re.search(r"^https://github.com/([a-zA-Z0-9\-_/]+)$", source_repo_url)
    if res is None:
        raise ValueError("Parameter source_repo_url is in unexpected format.")
    return res.groups()[0]


def _upload_assets(release_artifacts: Iterable[str], repo_id: str, release_id: int, content_type: str,
                   release_uploader: GithubReleaseAssetUploader, label_prefix: str):

    for release_artifact in release_artifacts:
        label = Path(release_artifact).name.split(".")[0]
        release_uploader.upload(archive_path=release_artifact,
                                label=f"{label_prefix} {label}",
                                repo_id=repo_id, release_id=release_id, content_type=content_type)


def release_upload(ctx: click.Context,
                   flavor_path: Tuple[str, ...],
                   source_repo_url: str,
                   release_id: int,
                   release_uploader: GithubReleaseAssetUploader) -> None:

    """
    Exports the container into tar.gz(s) and uploads to the repository / release.
    release_key is expected to have the following format: "{key}:{value}" where {key} can be:
    * "Tag"
    * "Id"
    source_repo_url is expected to have the following format: `https://github.com/exasol/script-languages-repo`
    """
    repo_id = _parse_repo_url(source_repo_url)
    with TemporaryDirectory() as temp_dir:
        logging.info(f"Running command 'export' with parameters: {locals()}")
        ctx.invoke(export, flavor_path=flavor_path, export_path=temp_dir, workers=7)
        _upload_assets(glob.glob(f'{temp_dir}/*.tar.gz'), repo_id, release_id,
                       "application/gzip", release_uploader, "Flavor")
        _upload_assets(glob.glob(f'{temp_dir}/*.tar.gz.sha512sum'), repo_id,
                       release_id, "text/plain", release_uploader, "Checksum")
