import dataclasses


@dataclasses.dataclass(frozen=True)
class TagInfo:
    tag_suffix: str
    build_step: str


EXPECTED_TAG_INFO_HASHES = [
    TagInfo(
        build_step="base_test_build_run",
        tag_suffix="GUA7R5J3UM27WOHJSQPX2OJNSIEKWCM5YF5GJXKKXZI53LZPV75Q",
    ),
    TagInfo(
        build_step="flavor_test_build_run",
        tag_suffix="G2OIMXJ2S3VS2EUAQNW4KWQLX3B2C27XYZ2SDMF7TQRS3UMAUWJQ",
    ),
    TagInfo(
        build_step="release",
        tag_suffix="MNWZZGSSFQ6VCLBDH7CZBEZC4K35QQBSLOW5DSYHF3DFFDX2OOZQ",
    ),
]

EXPECTED_LOCAL_TAG_INFO_HASHES = EXPECTED_TAG_INFO_HASHES + [
    TagInfo(
        build_step="security_scan",
        tag_suffix="JQFVF3LEHI7PQ5W6MCVODGJ3VKXPHDZSRCRLGSZJYNLHV2ALYYRQ",
    ),
]

BUILD_NAME = "test-build_1.2.3"

EXPECTED_TAG_INFO_RELEASE = [
    TagInfo(build_step="base_test_build_run", tag_suffix=BUILD_NAME),
    TagInfo(build_step="flavor_test_build_run", tag_suffix=BUILD_NAME),
    TagInfo(build_step="release", tag_suffix=BUILD_NAME),
]


EXPECTED_LOCAL_TAG_INFO_RELEASE = EXPECTED_TAG_INFO_RELEASE + [
    TagInfo(
        build_step="security_scan",
        tag_suffix=BUILD_NAME,
    ),
]
