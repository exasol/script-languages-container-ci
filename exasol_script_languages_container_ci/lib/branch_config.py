from enum import Enum, auto
import re


class BuildSteps(Enum):
    BUILD_ALL_ALWAYS = auto()
    TEST_ALWAYS = auto()
    REBUILD = auto()
    PUSH_TO_DOCKER_RELEASE_REPO = auto()


class BranchConfig(Enum):
    DEVELOP = {BuildSteps.BUILD_ALL_ALWAYS: True, BuildSteps.REBUILD: True, BuildSteps.TEST_ALWAYS: True,
               BuildSteps.PUSH_TO_DOCKER_RELEASE_REPO: False}
    MAIN = {BuildSteps.BUILD_ALL_ALWAYS: True, BuildSteps.REBUILD: True, BuildSteps.TEST_ALWAYS: True,
              BuildSteps.PUSH_TO_DOCKER_RELEASE_REPO: True}
    REBUILD = {BuildSteps.BUILD_ALL_ALWAYS: True, BuildSteps.REBUILD: True, BuildSteps.TEST_ALWAYS: True,
               BuildSteps.PUSH_TO_DOCKER_RELEASE_REPO: False}
    OTHER = {BuildSteps.BUILD_ALL_ALWAYS: False, BuildSteps.REBUILD: False, BuildSteps.TEST_ALWAYS: False,
             BuildSteps.PUSH_TO_DOCKER_RELEASE_REPO: False}

    @staticmethod
    def build_always(branch_name: str) -> bool:
        return get_branch_config(branch_name).value[BuildSteps.BUILD_ALL_ALWAYS]

    @staticmethod
    def test_always(branch_name) -> bool:
        return get_branch_config(branch_name).value[BuildSteps.TEST_ALWAYS]

    @staticmethod
    def rebuild(branch_name) -> bool:
        return get_branch_config(branch_name).value[BuildSteps.REBUILD]

    @staticmethod
    def push_to_docker_release_repo(branch_name: str) -> bool:
        return get_branch_config(branch_name).value[BuildSteps.PUSH_TO_DOCKER_RELEASE_REPO]


def get_branch_config(branch_name: str) -> BranchConfig:
    matches = ((re.compile(r"refs/heads/(master|main)"), BranchConfig.MASTER),
               (re.compile(r"refs/heads/develop"), BranchConfig.DEVELOP),
               (re.compile(r"refs/heads/rebuild/.*"), BranchConfig.REBUILD))

    branch_cfg = BranchConfig.OTHER
    for (branch_regex, branch_config) in matches:
        if branch_regex.match(branch_name):
            branch_cfg = branch_config
            break
    return branch_cfg
