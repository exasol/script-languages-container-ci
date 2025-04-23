from typing import List

from pydantic import BaseModel


class TestSet(BaseModel):
    name: str
    folders: List[str]


class TestConfig(BaseModel):
    test_runner: str
    test_sets: List[TestSet]


class FlavorCiConfig(BaseModel):
    build_runner: str
    test_config: TestConfig
