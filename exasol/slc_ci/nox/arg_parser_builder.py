import argparse

import nox


class ArgumentParserBuilder:
    def __init__(self, session: nox.Session) -> None:
        self._session = session
        self._usages = list()
        self._parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    def _add_arg(self, name: str):
        self._parser.add_argument(f"--{name}", required=True)
        self._usages.append(f"--{name} <{name}>")

    def with_flavor(self) -> "ArgumentParserBuilder":
        self._add_arg("flavor")
        return self

    def with_docker(self) -> "ArgumentParserBuilder":
        self._add_arg("docker-user")
        self._add_arg("docker-password")
        return self

    def with_testset(self) -> "ArgumentParserBuilder":
        self._add_arg("test-set-name")
        return self

    def with_slc_directory(self) -> "ArgumentParserBuilder":
        self._add_arg("slc-directory")
        return self

    def with_github_output(self) -> "ArgumentParserBuilder":
        self._add_arg("github-output")
        self._add_arg("github-var")
        return self

    def with_branch_name(self) -> "ArgumentParserBuilder":
        self._add_arg("branch-name")
        return self

    def with_commit_sha(self) -> "ArgumentParserBuilder":
        self._add_arg("commit-sha")
        return self

    def parse(self) -> argparse.Namespace:
        self._parser.usage = f"nox -s {self._session.name} {' '.join(self._usages)}"
        return self._parser.parse_args(self._session.posargs)
