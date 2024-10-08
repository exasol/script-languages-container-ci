import pytest

from exasol_script_languages_container_ci.lib.config.config_data_model import (
    Build,
    Config,
    Ignore,
    Release,
)


@pytest.fixture
def expected_config() -> Config:
    config = Config(
        build=Build(ignore=Ignore(paths=["a/b/c", "e/f/g"]), base_branch=""),
        release=Release(timeout_in_minutes=1),
    )
    return config


def test_serialization(expected_config, expected_json_config):
    actual_json = expected_config.model_dump_json(indent=4)
    assert actual_json == expected_json_config


def test_json_deserialization(expected_config, expected_json_config):
    actual_config = Config.parse_raw(expected_json_config)
    assert actual_config == expected_config
