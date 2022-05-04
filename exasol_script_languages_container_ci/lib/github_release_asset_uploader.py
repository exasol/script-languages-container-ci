import os
from pathlib import Path

from github import Github


class GithubReleaseAssetUploader(object):
    """
    Implements upload to a Github Release.
    See https://docs.github.com/en/rest/releases/assets#upload-a-release-asset for details.
    The access token needs to be stored in the environment variable GITHUB_TOKEN
    """
    def __init__(self):
        self._token = os.getenv("GITHUB_TOKEN")

    def upload(self, archive: Path, repo_id: str, release_id: int):
        gh = Github(self._token)
        gh_repo = gh.get_repo(repo_id)
        release = gh_repo.get_release(release_id)
        release.upload_asset(path=f"{archive}", label=f"Flavor {archive.name}")
