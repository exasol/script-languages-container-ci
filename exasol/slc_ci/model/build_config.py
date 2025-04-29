from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class BuildConfig:
    root: Path

    @property
    def flavors_path(self):
        return self.root / "flavors"

    base_branch: str
    ignore_paths: List[str]

    docker_build_repository: str
    docker_release_repository: str
    test_container_folder: str