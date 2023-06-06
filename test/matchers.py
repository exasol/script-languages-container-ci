import re
from pathlib import Path


class regex_matcher:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return f"{self._regex.pattern}"


class file_exists_matcher:

    def __eq__(self, actual):
        if not isinstance(actual, Path):
            return False
        if not actual.is_file():
            return False
        return actual.exists()

    def __repr__(self):
        return "file_exists"
