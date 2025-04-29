import exasol.slc_ci.lib.get_flavor_ci_model as lib_get_flavor_ci_model
from exasol.slc_ci.model.build_config import BuildConfig
from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig


def get_flavor_ci_model(build_config: BuildConfig, flavor: str) -> FlavorCiConfig:
    return lib_get_flavor_ci_model.get_flavor_ci_model(
        build_config=build_config, flavor=flavor
    )
