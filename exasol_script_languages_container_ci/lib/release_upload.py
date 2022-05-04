import logging
import glob
import re

from tempfile import TemporaryDirectory
from typing import Tuple, Sequence

import click
from exasol_script_languages_container_tool.cli.commands import export

from exasol_script_languages_container_ci.lib.github_release_asset_uploader import GithubReleaseAssetUploader


def _parse_upload_url(upload_url: str) -> Sequence:
    """
    upload_url is expected to have the following format: `https://uploads.github.com/repos/exasol/script-languages-repo/releases/123/assets{?name,label}`
    where `exasol/script-languages-repo` is the repository for which the release will be created and 123 is the id of the release.
    This method return thes repository and release id as tuple.
    """
    res = re.search(r"^https://uploads.github.com/repos/([a-zA-Z0-9\-_/]+)/releases/([\d]+)/assets", upload_url)
    if res is None:
        raise ValueError("Parameter upload_url is in unexpected format.")
    return res.groups()[0], int(res.groups()[1])


def release_upload(ctx: click.Context,
                   flavor_path: Tuple[str, ...],
                   upload_url: str,
                   release_uploader: GithubReleaseAssetUploader) -> None:

    """
    Export the container into a tar.gz and upload to the given url.
    upload_url is expected to have the following format: `https://uploads.github.com/repos/exasol/script-languages-repo/releases/123/assets{?name,label}`
    where `exasol/script-languages-repo` is the repository for which the release will be created and 123 is the id of the release.
    """
    repo_id, release_id = _parse_upload_url(upload_url)
    with TemporaryDirectory() as temp_dir:
        logging.info(f"Running command 'export' with parameters: {locals()}")
        ctx.invoke(export, flavor_path=flavor_path, export_path=temp_dir, workers=7)
        release_artifacts = glob.glob(f'{temp_dir}/*.tar.gz')
        for release_artifact in release_artifacts:
            release_uploader.upload(release_artifact, repo_id, release_id)
