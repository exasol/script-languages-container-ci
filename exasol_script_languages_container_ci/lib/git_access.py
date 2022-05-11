from typing import Iterable

from git import Repo


class GitAccess:

    def get_last_commit_message(self):
        """
        Assumes that PWD belongs to a GIT repository. Get's the last commit message of this repo and returns it as string
        :return: Last commit message of current working directory GIT repository.
        """
        return Repo().head.commit.message

    def get_files_of_last_commit(self) -> Iterable[str]:
        """
        Returns the files of the last commit of the repo in the cwd.
        """
        repo = Repo()
        commit = repo.head.commit
        return commit.stats.files.keys()

