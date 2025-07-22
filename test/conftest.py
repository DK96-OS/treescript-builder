""" Test Fixtures and Data Providers.
"""
import pytest

from pathlib import Path

from treescript_builder.data.instruction_data import InstructionData


# Data Tree Target Paths
DATA_TREE_TARGET_DIR_NAME = "target_dir"
DATA_TREE_TARGET_FILE_NAME = "target_file.txt"
DATA_TREE_TARGET_FILE_CONTENTS = "Target File Contents."

# Data Tree Data Paths
DATA_TREE_DATA_DIR_NAME = "data_dir"
DATA_TREE_DATA_FILE_NAME = "data_file.txt"
DATA_TREE_DATA_FILE_CONTENTS = "Data File Contents."

# Data Tree Instructions
DATA_TREE_TARGET_DIR_INSTRUCT = InstructionData(True, Path('./target_dir/'), None)
DATA_TREE_DATA_DIR_INSTRUCT = InstructionData(True, Path('./data_dir/'), None)
DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA = InstructionData(False, Path('./target_dir/target_file.txt'), None)
DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA = InstructionData(False, Path('./target_dir/target_file.txt'), Path('./data_dir/data_file.txt'))


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
    
    
def create_data_tree(
    root_dir: Path,
    initial_target_content: bool = False,
):
    """ Creates the Data Tree with unique text content in the Target File and the Data File.
    """
    (target_dir := root_dir / DATA_TREE_TARGET_DIR_NAME).mkdir()
    (target_file := target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
    (data_dir := root_dir / DATA_TREE_DATA_DIR_NAME).mkdir()
    (data_file := data_dir / DATA_TREE_DATA_FILE_NAME).touch()
    data_file.write_text(DATA_TREE_DATA_FILE_CONTENTS)
    if initial_target_content:
        target_file.write_text(DATA_TREE_TARGET_FILE_CONTENTS)


@pytest.fixture
def mock_data_tree(temp_cwd):
    """ A File Tree, where files contain just single line of text.
    """
    (target_dir := Path(temp_cwd.name) / DATA_TREE_TARGET_DIR_NAME).mkdir()
    (target_file := target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
    target_file.write_text(DATA_TREE_TARGET_FILE_CONTENTS)
    (data_dir := Path(temp_cwd.name) / DATA_TREE_DATA_DIR_NAME).mkdir()
    (data_file := data_dir / DATA_TREE_DATA_FILE_NAME).touch()
    data_file.write_text(DATA_TREE_DATA_FILE_CONTENTS)
    return Path(str(temp_cwd.name))


@pytest.fixture
def mock_data_tree_empty(temp_cwd):
    """ Similar to the data tree, but all files are empty.
    """
    (target_dir := Path(temp_cwd.name) / DATA_TREE_TARGET_DIR_NAME).mkdir()
    (target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
    (data_dir := Path(temp_cwd.name) / DATA_TREE_DATA_DIR_NAME).mkdir()
    (data_dir / DATA_TREE_DATA_FILE_NAME).touch()
    return Path(str(temp_cwd.name))
