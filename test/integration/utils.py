import contextlib
from pathlib import Path

from exasol.slc.api import clean_flavor_images


@contextlib.contextmanager
def cleanup_images(flavor_path: Path):
    clean_flavor_images(
        flavor_path=(str(flavor_path),),
    )
    yield
    clean_flavor_images(
        flavor_path=(str(flavor_path),),
    )
