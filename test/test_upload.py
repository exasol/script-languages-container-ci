from pathlib import Path
from unittest.mock import MagicMock, call

from exasol_script_languages_container_ci.lib.release_upload import release_upload


class ClickExportMock:
    """Helper class which which simulates the creation of the release artifacts"""

    def invoke(self, method, flavor_path, export_path, workers):
        if method.name == "export":
            with open(f"{export_path}/abc.tar.gz", "w") as f:
                pass
            with open(f"{export_path}/abc.tar.gz.sha512sum", "w") as f:
                pass
            with open(f"{export_path}/def-8.0.tar.gz", "w") as f:
                pass
            with open(f"{export_path}/def-8.0.tar.gz.sha512sum", "w") as f:
                pass
        else:
            raise RuntimeError(f"Unexpected method invoked: {method}")


class ComparePathAppendix(str):
    """
    Helper class which compares only the appendix of the a path with the given file-names
    """

    def __eq__(self, other: Path):
        return str(other).endswith(self)


def test_upload_release_id():
    """
    Test that release_upload() will:
     1. Export the container
     2. Call upload for all resulting tar.gz
    """
    REPO_ID = "exasol/script-languages-repo"
    REPO_URL = f"https://github.com/{REPO_ID}"
    RELEASE_ID = 123
    release_uploader = MagicMock()
    release_upload(ClickExportMock(), flavor_path=("test-flavor",), source_repo_url=REPO_URL,
                   release_id=RELEASE_ID, release_uploader=release_uploader)
    upload_args = release_uploader.upload.call_args_list
    # Compare both dummy filenames here because we don't have guarantee regarding the order of the file-system will read them
    # Important to keep the expression with ComparePathAppendix on the left side!
    assert len(upload_args) == 4 and \
           (call(archive_path=ComparePathAppendix("abc.tar.gz"), label="Flavor abc",
                 repo_id=REPO_ID, release_id=RELEASE_ID, content_type="application/gzip") in upload_args and
            call(archive_path=ComparePathAppendix("abc.tar.gz.sha512sum"), label="Checksum abc",
                 repo_id=REPO_ID, release_id=RELEASE_ID, content_type="text/plain") in upload_args and
            call(archive_path=ComparePathAppendix("def-8.0.tar.gz"), label="Flavor def-8.0",
                 repo_id=REPO_ID, release_id=RELEASE_ID, content_type="application/gzip") in upload_args and

            call(archive_path=ComparePathAppendix("def-8.0.tar.gz.sha512sum"), label="Checksum def-8.0",
                 repo_id=REPO_ID, release_id=RELEASE_ID, content_type="text/plain") in upload_args)
