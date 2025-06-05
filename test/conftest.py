import logging
import os
from tempfile import TemporaryDirectory
from test.unit.fixtures import *
from test.integration.fixtures import *
from unittest import mock
from unittest.mock import MagicMock

script_path = Path(__file__).absolute().parent

logger = logging.getLogger(__name__)


@pytest.fixture()
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {}):
        yield


@pytest.fixture(autouse=True)
def tmp_test_dir():
    """
    Change cwd to a tmp directory for executing tests. Thus, we avoid any possible interference (git repository).
    :return:
    """
    with TemporaryDirectory() as temp_dir:
        old_dir = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(old_dir)


@pytest.fixture()
def git_access_mock():
    """
    Return an object which mocks the git access class. The mock object returns some default values useful for the tests.
    """
    git_access_mock = MagicMock()
    git_access_mock.get_last_commits.return_value = ["456", "123"]
    git_access_mock.get_head_commit_sha_of_branch.return_value = "123"
    git_access_mock.get_files_of_commit.return_value = ["src/udfclient.cpp"]
    git_access_mock.get_last_commit_message.return_value = "last commit"
    return git_access_mock
