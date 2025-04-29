from pathlib import Path
from typing import Iterable


def get_flavors(flavors_path: Path) -> Iterable[str]:
    if not flavors_path.exists():
        raise ValueError(f"{flavors_path} does not exist")
    for p in flavors_path.iterdir():
        if p.is_dir():
            yield p.name
