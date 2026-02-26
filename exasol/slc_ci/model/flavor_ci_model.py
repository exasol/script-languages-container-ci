from exasol.slc.models.accelerator import Accelerator
from pydantic import BaseModel


class TestSet(BaseModel):
    name: str
    files: list[str]
    folders: list[str]
    goal: str
    generic_language_tests: list[str]
    test_runner: list[str] | None = None # the values can be x86_64 or arm64
    accelerator: Accelerator = Accelerator.NONE


class TestConfig(BaseModel):
    default_test_runner: list[str] # the values can be x86_64 or arm64
    test_sets: list[TestSet]


class FlavorCiConfig(BaseModel):
    build_runner: list[str] # the values can be x86_64 or arm64
    test_config: TestConfig
