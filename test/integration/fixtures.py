from pathlib import Path

import pytest

script_path = Path(__file__).absolute().parent


@pytest.fixture
def resources_path() -> Path:
    return script_path / "resources"


@pytest.fixture
def flavors_path(resources_path: Path) -> Path:
    return resources_path / "flavors"


@pytest.fixture
def test_containers_folder(resources_path: Path) -> Path:
    return resources_path / "test_containers"