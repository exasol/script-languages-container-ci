import logging
import glob
import re
from pathlib import Path

from tempfile import TemporaryDirectory
from typing import Tuple, Union

import click
from exasol_script_languages_container_tool.cli.commands import export

from exasol_script_languages_container_ci.lib.github_release_asset_uploader import GithubReleaseAssetUploader


def _parse_release_key(release_key: str) -> Union[str, int]:
    """
    Release key is expected to be in format: "{key}:{value}" where {key} can be:
    * "Tag"
    * "Id"
    This functions returns the tag as string if the prefix is "Tag:", the release id as integer otherwise.
    """
    if release_key.startswith("Tag:"):
        return release_key[len("Tag:"):]
    elif release_key.startswith("Id:"):
        res = re.search(r"^Id:([\d]+)$", release_key)
        if res is None:
            raise ValueError("Parameter release_key is in unexpected format.")
        return int(res.groups()[0])
    else:
        raise ValueError("Parameter release_key is in unexpected format.")


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
                   release_key: str,
                   release_uploader: GithubReleaseAssetUploader) -> None:

    """
    Exports the container into tar.gz(s) and uploads to the repository / release.
    release_key is expected to have the following format: "{key}:{value}" where {key} can be:
    * "Tag"
    * "Id"
    source_repo_url is expected to have the following format: `https://github.com/exasol/script-languages-repo`
    """
    release_id = _parse_release_key(release_key)
    repo_id = _parse_repo_url(source_repo_url)
    with TemporaryDirectory() as temp_dir:
        logging.info(f"Running command 'export' with parameters: {locals()}")
        ctx.invoke(export, flavor_path=flavor_path, export_path=temp_dir, workers=7)
        release_artifacts = glob.glob(f'{temp_dir}/*.tar.gz')
        for release_artifact in release_artifacts:
            release_uploader.upload(archive_path=release_artifact,
                                    label=f"Flavor {Path(release_artifact).with_suffix('').stem}",
                                    repo_id=repo_id, release_id=release_id, content_type="application/gzip")
