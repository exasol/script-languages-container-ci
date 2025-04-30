import json

import pytest
from pydantic import ValidationError

from exasol.slc_ci.lib.get_build_config_model import get_build_config_model


def test_get_build_config_model(build_config_environment):
    res_build_config = get_build_config_model()
    assert res_build_config == build_config_environment


def test_get_build_config_model_fails_with_invalid_json(build_config, tmp_test_dir):
    build_config_json = build_config.model_dump_json()
    build_config_obj = json.loads(build_config_json)
    del build_config_obj["ignore_paths"]
    with open("build_config.json", "w") as f:
        json.dump(build_config_obj, f)

    with pytest.raises(ValidationError):
        get_build_config_model()
