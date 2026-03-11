import platform

from exasol.slc_ci.lib.github_access import GithubAccess


def get_platform(github_access: GithubAccess):
    """
    Detects the platform of the current runner and sets it as a GitHub Actions output.
    """
    machine = platform.machine()
    github_access.write_result(machine)
