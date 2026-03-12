import json

from exasol.slc.models.flavor_ci_model import FlavorCiConfig, TestSet

from exasol.slc_ci.lib.get_build_config_model import get_build_config_model
from exasol.slc_ci.lib.get_flavor_ci_model import get_flavor_ci_model
from exasol.slc_ci.lib.github_access import GithubAccess


def _build_test_matrix_entry(
    flavor_config: FlavorCiConfig, test_set: TestSet
) -> list[dict]:
    runners = (
        test_set.test_runners
        if test_set.test_runners
        else flavor_config.test_config.default_test_runners
    )

    entries: list[dict] = []
    for runner in runners:
        entries.append(
            {
                "test-set-name": test_set.name,
                "test-runner": runner,
                "goal": test_set.goal,
            }
        )
    return entries


def get_test_matrix(flavor: str, github_access: GithubAccess):
    build_config = get_build_config_model()
    flavor_config = get_flavor_ci_model(build_config, flavor)

    include_entries: list[dict] = [
        item
        for entry in flavor_config.test_config.test_sets
        for item in _build_test_matrix_entry(flavor_config, entry)
    ]

    test_matrix = {"include": include_entries}
    github_access.write_result(json.dumps(test_matrix))
