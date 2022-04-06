import os

from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch, MagicMock

import click
import pytest
import exasol_script_languages_container_ci


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


@pytest.fixture
def click_stub():
    click_ctx = click.Context(command=click.Command("dummy"))
    return Mock(click_ctx)




@pytest.fixture(autouse=True)
def patch_printfile():
    """
    This overwrites automatically function "exasol_script_languages_container_ci.lib.print_file" because within the UnitTests
    the output files are not being created. Also accelerate Unit-Tests by avoiding file-access.
    """
    with patch('exasol_script_languages_container_ci.lib.print_file', MagicMock()):
        yield
