import os
import re
from contextlib import contextmanager

import pytest
from _pytest.monkeypatch import MonkeyPatch

from exasol.slc_ci.model.build_config_model import BuildConfig



@pytest.fixture
def build_config():
    return BuildConfig(base_branch="master",
                       ignore_paths=["doc", "githooks"],
                       docker_build_repository="test/script-languages-build-cache",
                       docker_release_repository="test/script-language-container",
                       test_container_folder="test_container",)

@pytest.fixture
def build_config_environment(tmp_test_dir, build_config):
    with open("build_config.json", "w") as f:
        f.write(build_config.model_dump_json())
    return build_config

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

