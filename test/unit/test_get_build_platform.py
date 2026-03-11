import platform

import pytest
from _pytest.monkeypatch import MonkeyPatch

from unittest.mock import MagicMock

from exasol.slc_ci.lib.get_platform import (
    get_platform as lib_get_platform,
)

@pytest.fixture
def platform_mock(monkeypatch: MonkeyPatch):
    mock_function_to_mock = MagicMock()
    monkeypatch.setattr(platform, "machine", mock_function_to_mock)
    return mock_function_to_mock

def test_get_build_runners(platform_mock):
    platform_value = "test_platform"
    platform_mock.return_value = platform_value
    github_output_mock = MagicMock()
    lib_get_platform(github_output_mock)
    assert (
        github_output_mock.write_result.call_args.args[0]
        == platform_value
    )
