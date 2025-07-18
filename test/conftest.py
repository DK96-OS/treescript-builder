""" Test Fixtures and Data Providers.
"""
import pytest

from pathlib import Path


@pytest.fixture
def temp_cwd():
    """ Creates a Temporary Working Directory for Git subprocesses.
    """
    from tempfile import TemporaryDirectory
    tdir = TemporaryDirectory()
    from os import getcwd, chdir
    initial_cwd = getcwd()
    chdir(tdir.name)
    yield tdir
    chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def mock_basic_tree(temp_cwd):
    (src_dir := Path(temp_cwd.name) / 'src').mkdir()
    (src_dir / 'data.txt').touch()
    return Path(str(temp_cwd))


@pytest.fixture
def mock_data_tree(temp_cwd):
    (target_dir := Path(temp_cwd.name) / 'target_dir/').mkdir()
    (target_file := target_dir / 'target_file.txt').touch()
    target_file.write_text("Target File Contents.")
    (data_dir := Path(temp_cwd.name) / 'data_dir/').mkdir()
    (data_file := data_dir / 'data_file.txt').touch()
    data_file.write_text("Data File Contents.")
    return Path(str(temp_cwd.name))
