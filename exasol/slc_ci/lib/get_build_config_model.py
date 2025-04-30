from pathlib import Path

from exasol.slc_ci.model.build_config_model import BuildConfig


def get_build_config_model() -> BuildConfig:
    build_config_path = Path.cwd() / "build_config.json"
    return BuildConfig.model_validate_json(
        build_config_path.read_text(), strict=True
    )
