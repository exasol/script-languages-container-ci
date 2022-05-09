import logging
import glob
import re
from pathlib import Path

from tempfile import TemporaryDirectory
from typing import Tuple

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
        release_artifacts = glob.glob(f'{temp_dir}/*.tar.gz') + glob.glob("{temp_dir}/*.tar.gz.sha512sum")
        for release_artifact in release_artifacts:
            release_uploader.upload(archive_path=release_artifact,
                                    label=f"Flavor {Path(release_artifact).with_suffix('').stem}",
                                    repo_id=repo_id, release_id=release_id, content_type="application/gzip")
