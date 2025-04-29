from test.unit.v2.resources.slc_build_config import SLC_BUILD_CONFIG

from exasol.slc_ci.model.flavor_ci_model import FlavorCiConfig, TestConfig, TestSet


class TestEnv:
    docker_user = "test_docker_user"
    docker_pwd = "test_docker_pwd"
    commit_sha = "test_commit_sha"
    branch_name = "test_branch_name"
    build_config = SLC_BUILD_CONFIG
    flavor_config = FlavorCiConfig(
        build_runner="some_build_runner",
        test_config=TestConfig(
            test_runner="some_test_runner",
            test_sets=[TestSet(name="some_test_name", folders=["all", "specific"])],
        ),
    )


test_env = TestEnv()
