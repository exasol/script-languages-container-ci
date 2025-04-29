from typing import Iterable

import exasol.slc_ci.lib.get_flavors as lib_get_flavors
from exasol.slc_ci.model.build_config import BuildConfig


def get_flavors(build_config: BuildConfig) -> Iterable[str]:
    yield from lib_get_flavors.get_flavors(build_config=build_config)
