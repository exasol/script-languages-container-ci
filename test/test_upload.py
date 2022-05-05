from pathlib import Path
from typing import List
from unittest.mock import MagicMock, call

from exasol_script_languages_container_ci.lib.release_upload import release_upload


class ClickUploadMock:
    """Helper class which which simulates the created """

    def invoke(self, method, flavor_path, export_path, workers):
        if method.name == "export":
            with open(f"{export_path}/abc.tar.gz", "w") as f:
                pass
            with open(f"{export_path}/def.tar.gz", "w") as f:
                pass
        else:
            raise RuntimeError(f"Unexpected method invoked: {method}")


class ComparePathAppendix(str):
    """
    Helper class which compares only the appendix of the a path with the given file-names
    """

    def __eq__(self, other: Path):
        return str(other).endswith(self)


def test_upload():
    """
    Test that release_upload() will:
     1. Export the container
     2. Call upload for all resulting tar.gz
    """
    REPO_ID = "exasol/script-languages-repo"
    RELEASE_ID = 123456
    UPLOAD_URL = f"https://uploads.github.com/repos/{REPO_ID}/releases/{RELEASE_ID}/assets{{?name,label}}"
    release_uploader = MagicMock()
    release_upload(ClickUploadMock(), flavor_path=("test-flavor",), upload_url=UPLOAD_URL,
                   release_uploader=release_uploader)
    upload_args = release_uploader.upload.call_args_list
    assert len(upload_args) == 2
    # Compare both dummy filenames here because we don't have guarantee regarding the order of the file-system will read them
    # Important to keep the expression with ComparePathAppendix on the left side!
    assert call(archive_path=ComparePathAppendix("abc.tar.gz"), label="Flavor abc",
                repo_id=REPO_ID, release_id=RELEASE_ID) == upload_args[0] or \
           call(archive_path=ComparePathAppendix("def.tar.gz"), label="Flavor def",
                repo_id=REPO_ID, release_id=RELEASE_ID) == upload_args[0]
    assert call(archive_path=ComparePathAppendix("abc.tar.gz"), label="Flavor abc",
                repo_id=REPO_ID, release_id=RELEASE_ID) == upload_args[1] or \
           call(archive_path=ComparePathAppendix("def.tar.gz"), label="Flavor def",
                repo_id=REPO_ID, release_id=RELEASE_ID) == upload_args[1]
