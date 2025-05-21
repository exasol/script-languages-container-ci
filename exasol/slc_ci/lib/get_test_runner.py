from exasol.slc_ci.lib.get_build_config_model import get_build_config_model
from exasol.slc_ci.lib.get_flavor_ci_model import get_flavor_ci_model
from exasol.slc_ci.lib.github_access import GithubAccess


def get_test_runner(flavor: str, test_set_name: str, github_access: GithubAccess):
    build_config = get_build_config_model()
    flavor_config = get_flavor_ci_model(build_config, flavor)
    matched_test_set = [
        test_set
        for test_set in flavor_config.test_config.test_sets
        if test_set.name == test_set_name
    ]
    if len(matched_test_set) != 1:
        raise ValueError(f"Invalid test set name: {test_set_name}")
    if matched_test_set[0].test_runner:
        github_access.write_result(matched_test_set[0].test_runner)
    else:
        github_access.write_result(flavor_config.test_config.default_test_runner)
