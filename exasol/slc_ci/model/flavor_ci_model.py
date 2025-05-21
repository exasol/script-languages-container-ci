from typing import List, Optional

from pydantic import BaseModel


class TestSet(BaseModel):
    name: str
    folders: List[str]
    goal: str
    generic_language_tests: List[str]
    test_runner: Optional[str] = None


class TestConfig(BaseModel):
    default_test_runner: str
    test_sets: List[TestSet]


class FlavorCiConfig(BaseModel):
    build_runner: str
    test_config: TestConfig
