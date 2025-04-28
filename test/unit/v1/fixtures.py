from inspect import cleandoc

import pytest

from exasol_script_languages_container_ci.lib.config.config_data_model import Config, Build, Ignore, Release


@pytest.fixture
def build_config() -> Config:
    return Config(
        build=Build(ignore=Ignore(paths=["doc"]), base_branch="master"),
        release=Release(timeout_in_minutes=1),
    )


@pytest.fixture
def expected_json_config() -> str:
    json = cleandoc(
        """
    {
        "build": {
            "ignore": {
                "paths": [
                    "a/b/c",
                    "e/f/g"
                ]
            },
            "base_branch": ""
        },
        "release": {
            "timeout_in_minutes": 1
        }
    }"""
    )
    return json
