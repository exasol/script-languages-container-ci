import pytest


from exasol.slc_ci.model.build_config_model import BuildConfig



@pytest.fixture
def build_config():
    return BuildConfig(base_branch="master",
                       ignore_paths=["doc", "githooks"],
                       docker_build_repository="test/script-languages-build-cache",
                       docker_release_repository="test/script-language-container",
                       test_container_folder="test_container",)

@pytest.fixture
def build_config_environment(tmp_test_dir, build_config):
    with open("build_config.json", "w") as f:
        f.write(build_config.model_dump_json())
    return build_config

