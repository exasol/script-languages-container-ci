from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from nox import Session


@dataclass(frozen=True)
class Config:
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
    python_versions = ["3.9", "3.10", "3.11", "3.12", "3.13"]


PROJECT_CONFIG = Config()
