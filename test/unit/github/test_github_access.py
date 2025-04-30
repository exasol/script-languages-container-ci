import re

import pytest
from _pytest.monkeypatch import MonkeyPatch

from exasol.slc_ci.lib.github_access import GithubAccess


@pytest.fixture
def github_output(monkeypatch: MonkeyPatch, tmp_path):
    out_file = tmp_path / "out.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))
    return out_file

@pytest.fixture
def github_output_reader(github_output):
    def reader(github_var: str):
        pattern = f'{github_var}=(.+)'
        match = re.search(pattern, github_output.read_text())
        assert match
        return match.group(1)
    return reader

def test_github_access(github_output_reader):
    github_access = GithubAccess("result")
    github_access.write_result("something")
    res = github_output_reader("result")
    assert res == "something"