from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from exasol.toolbox.config import BaseConfig


class Config(BaseConfig):
    root: Path = Path(__file__).parent
    source: Path = Path(__file__).parent / "exasol"
    doc: Path = Path(__file__).parent / "doc"
    version_file: Path = Path(__file__).parent / "exasol" / "slc_ci" / "version.py"
    path_filters: Iterable[str] = (
        "dist",
        ".eggs",
        "venv",
        "resources",
        "config_data_model.py",
    )


PROJECT_CONFIG = Config(python_versions=("3.10", "3.11", "3.12", "3.13"), exasol_versions=(), create_major_version_tags=False)
