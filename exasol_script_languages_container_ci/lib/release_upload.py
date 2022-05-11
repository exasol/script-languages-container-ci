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


def _upload_assets(repo_id: str, release_id: int, content_type: str,
                   release_uploader: GithubReleaseAssetUploader, artifact_path: str,
                   file_suffix: str, label_prefix: str):
    release_artifacts = glob.glob(f'{artifact_path}/*{file_suffix}')
    for release_artifact in release_artifacts:
        artifact_file_name = Path(release_artifact).name
        if artifact_file_name.endswith(file_suffix):
            artifact_file_name = artifact_file_name[:-len(file_suffix)]
        else:
            logging.error(f"Artifact file: {artifact_file_name} does not end with {file_suffix}. "
                          f"Using {artifact_file_name} as label.")
        release_uploader.upload(archive_path=release_artifact,
                                label=f"{label_prefix} {artifact_file_name}",
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
        _upload_assets(repo_id, release_id, "application/gzip", release_uploader, temp_dir, ".tar.gz", "Flavor")
        _upload_assets(repo_id, release_id, "text/plain", release_uploader, temp_dir, ".tar.gz.sha512sum", "Checksum")
