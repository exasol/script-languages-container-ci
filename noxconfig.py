from __future__ import annotations

from pathlib import Path

from exasol.toolbox.config import BaseConfig
from pydantic import computed_field


class Config(BaseConfig):
    @computed_field  # type: ignore[misc]
    @property
    def has_documentation(self) -> bool:
        """
        Indicates that the project serves Sphinx-based documentation. With a few
        exceptions, this should be the case for most projects.
        """
        return False

    @computed_field  # type: ignore[misc]
    @property
    def integration_test_targets(self) -> list[str]:
        """
        Return integration test target groups used to shard slow CI runs.

        Each target is the stem of a test module under ``test/integration`` and is
        used as a pytest ``-k`` expression in the workflow matrix.
        """
        test_root = self.root_path / "test" / "integration"
        return sorted(
            path.stem
            for path in test_root.glob("test_*.py")
            if path.name != "__init__.py"
        )


PROJECT_CONFIG = Config(
    root_path=Path(__file__).parent,
    project_name="slc_ci",
    python_versions=("3.10", "3.11", "3.12", "3.13"),
    exasol_versions=(),
    add_to_excluded_python_paths=("test/integration/resources",),
)
