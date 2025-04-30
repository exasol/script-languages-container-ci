from exasol.slc_ci.lib.get_build_config_model import get_build_config_model
from exasol.slc_ci.lib.get_flavor_ci_model import get_flavor_ci_model
from exasol.slc_ci.lib.write_github_var import write_github_var


def get_build_runner(flavor: str, github_var: str):
    build_config = get_build_config_model()
    flavor_config = get_flavor_ci_model(build_config, flavor)
    write_github_var(github_var, flavor_config.build_runner)