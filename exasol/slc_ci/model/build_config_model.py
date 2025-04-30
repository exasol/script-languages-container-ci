from pathlib import Path
from typing import List

from pydantic import BaseModel


class BuildConfig(BaseModel):

    @property
    def root_path(self) -> Path:
        return Path.cwd()

    @property
    def flavors_path(self):
        return self.root_path / "flavors"

    ignore_paths: List[str]

    docker_build_repository: str
    docker_release_repository: str
    test_container_folder: str
