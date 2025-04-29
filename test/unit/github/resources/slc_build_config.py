from pathlib import Path

from exasol.slc_ci.model.build_config import BuildConfig

SLC_BUILD_CONFIG = BuildConfig(root=Path(__file__).parent, base_branch="master",
                               ignore_paths=["doc", "githooks"],
                               docker_build_repository="test/script-languages-build-cache",
                               docker_release_repository="test/script-language-container",
                               test_container_folder="test_container", )
