from github import Github


class GithubReleaseAssetUploader(object):
    """
    Implements upload to a Github Release.
    See https://docs.github.com/en/rest/releases/assets#upload-a-release-asset for details.
    The access token needs to be stored in the environment variable GITHUB_TOKEN
    """
    def __init__(self, token):
        self._token = token

    def upload(self, archive_path: str, label: str, repo_id: str, release_id: int, content_type: str):
        gh = Github(self._token)
        gh_repo = gh.get_repo(repo_id)
        release = gh_repo.get_release(release_id)
        release.upload_asset(path=archive_path, label=label, content_type=content_type)
