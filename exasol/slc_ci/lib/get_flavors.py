from typing import Iterable

from exasol.slc_ci.model.build_config import BuildConfig


def get_flavors(build_config: BuildConfig) -> Iterable[str]:
    if not build_config.flavors_path.exists():
        raise ValueError(f"{build_config.flavors_path} does not exist")
    for p in build_config.flavors_path.iterdir():
        if p.is_dir():
            yield p.name
