from enum import Enum


class BuildMode(Enum):
    """
    This enum serves as a definition of values for possible build modes.
    """

    NORMAL = "normal"
    REBUILD = "rebuild"
    RELEASE = "release"


def buildModeValues() -> list[str]:
    return [a.value for a in BuildMode]


def defaultBuildMode() -> BuildMode:
    return BuildMode.NORMAL
