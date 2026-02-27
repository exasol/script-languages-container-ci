from exasol.slc.models.accelerator import Accelerator
from pydantic import BaseModel

# Values for runners be like ["ubuntu-24.04, x64_64", "ubuntu-24.04, arm64"]
class TestSet(BaseModel):
    name: str
    files: list[str]
    folders: list[str]
    goal: str
    generic_language_tests: list[str]
    test_runners: list[str] | None = None
    accelerator: Accelerator = Accelerator.NONE


class TestConfig(BaseModel):
    default_test_runners: list[str]
    test_sets: list[TestSet]


class FlavorCiConfig(BaseModel):
    build_runners: list[str]
    test_config: TestConfig
