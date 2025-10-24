""" Test Fixtures and Data Providers.
 - Selection of TreeScript: Basic, Nested, EmptyDirs.
 - TempPath FileTree Fixtures.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from treescript_builder.data.control_modes import ControlMode
from treescript_builder.data.input_data import InputData
from treescript_builder.data.instruction_data import InstructionData

TEST_INPUT_FILE = 'input.tree'
TEST_DATA_DIR = 'data/dir'

# Data Tree Target Paths
DATA_TREE_TARGET_DIR_NAME = "target_dir"
DATA_TREE_TARGET_FILE_NAME = "target_file.txt"
DATA_TREE_TARGET_FILE_CONTENTS = "Target File Contents."

# Data Tree Data Paths
DATA_TREE_DATA_DIR_NAME = "data_dir"
DATA_TREE_DATA_FILE_NAME = "data_file.txt" # AKA DataLabel
DATA_TREE_DATA_FILE_CONTENTS = "Data File Contents."

# Data Tree Instructions
DATA_TREE_TARGET_DIR_INSTRUCT = InstructionData(True, Path(f'./{DATA_TREE_TARGET_DIR_NAME}/'), None)
DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA = InstructionData(False, Path(f'./{DATA_TREE_TARGET_DIR_NAME}/{DATA_TREE_TARGET_FILE_NAME}'), None)
DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA = InstructionData(False, Path(f'./{DATA_TREE_TARGET_DIR_NAME}/{DATA_TREE_DATA_FILE_NAME}'), Path(f'./{DATA_TREE_DATA_DIR_NAME}/{DATA_TREE_DATA_FILE_NAME}'))


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
def mock_data_tree_empty_data_dir(temp_cwd):
    """ A File Tree, where files contain just single line of text.
    """
    (target_dir := Path(temp_cwd.name) / DATA_TREE_TARGET_DIR_NAME).mkdir()
    (target_file := target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
    target_file.write_text(DATA_TREE_TARGET_FILE_CONTENTS)
    (data_dir := Path(temp_cwd.name) / DATA_TREE_DATA_DIR_NAME).mkdir()
    return Path(str(temp_cwd.name))


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


def get_data_tree_instructions(
    with_data: bool = True,
    is_trim: bool = False,
) -> tuple[InstructionData, ...]:
    """ Obtain InstructionData Tuples for the DataTree.
 - Provides both Trim and Build Instruction Tuples. Note: In Trim Operations, Files are Trimmed before Directories.

**Parameters:**
 - with_data (bool): Whether to include the DataLabel. Default: True.
 - is_trim (bool): Whether the Instructions are for Trim Operations. Default: False.

**Returns:**
 tuple[InstructionData] - The Instruction Tuple containing the DataTree Paths, for the requested operation.
    """
    if is_trim:
        return (DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA, DATA_TREE_TARGET_DIR_INSTRUCT) \
            if with_data else (DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA, DATA_TREE_TARGET_DIR_INSTRUCT)
    else: # Build (reverse files and dir instructions)
        return (DATA_TREE_TARGET_DIR_INSTRUCT, DATA_TREE_TARGET_FILE_INSTRUCT_WITH_DATA) \
            if with_data else (DATA_TREE_TARGET_DIR_INSTRUCT, DATA_TREE_TARGET_FILE_INSTRUCT_NO_DATA)


@pytest.fixture
def mock_data_tree_empty(temp_cwd):
    """ Similar to the data tree, but all files are empty.
    """
    (target_dir := Path(temp_cwd.name) / DATA_TREE_TARGET_DIR_NAME).mkdir()
    (target_dir / DATA_TREE_TARGET_FILE_NAME).touch()
    (data_dir := Path(temp_cwd.name) / DATA_TREE_DATA_DIR_NAME).mkdir()
    (data_dir / DATA_TREE_DATA_FILE_NAME).touch()
    return Path(str(temp_cwd.name))


def get_basic_tree_script() -> str:
    return 'src/\n  data.txt'


def get_basic_tree_build_instructions(data_file_path: Path | None = None) -> tuple[InstructionData, ...]:
    return (
        InstructionData(True, Path('src/'), None),
        InstructionData(False, Path('src/data.txt'), data_file_path),
    )


def get_basic_tree_trim_instructions(data_file_path: Path | None = None) -> tuple[InstructionData, ...]:
    return (
        InstructionData(False, Path('src/data.txt'), data_file_path),
        InstructionData(True, Path('src/'), None),
    )


def get_basic_data_tree_script() -> str:
    return 'src/\n  data.txt DataLabel'


def get_data_tree_script() -> str:
    return f'{DATA_TREE_TARGET_DIR_NAME}/\n  {DATA_TREE_TARGET_FILE_NAME} {DATA_TREE_DATA_FILE_NAME}'


def get_nested_tree_script() -> str:
    return 'src/\n  main/\n    SourceClass.java'


def get_empty_dirs_tree_script() -> str:
    return 'empty_dirs/\n  dir1/\n  dir2/\n  dir3/'


def get_hidden_tree_script() -> str:
    return """.github/
  dependabot.yml
  workflows/
    ci.yml
.hidden.txt
"""


TS_INPUT_STR_1 = 'src/\n  main_src_file.code'


def get_treescript_input_sample(
    tree_sample_name: str,
) -> str:
    """ Obtain a TreeScript input string sample from this conftest collection.

**Parameters:**
 - tree_sample_name (str): The name of the TreeScript sample.

**Returns:**
 str - The TreeScript sample that was requested.

**Raises:**
 ValueError - When the given parameter is not recognized.
    """
    match tree_sample_name.lower():
        case 'input.tree':
            return TS_INPUT_STR_1
        case 'data_tree':
            return get_data_tree_script()
        case 'basic':
            return get_basic_tree_script()
        case 'basic+data':
            return get_basic_data_tree_script()
        case 'nested':
            return get_nested_tree_script()
        case 'empty_dirs':
            return get_empty_dirs_tree_script()
        case 'hidden':
            return get_hidden_tree_script()
    raise ValueError(f'Unknown TreeScript Input Sample: {tree_sample_name}')


@pytest.fixture
def mock_basic_tree(tmp_path):
    (src_dir := tmp_path / 'src').mkdir()
    (src_dir / 'data.txt').touch()
    (ts_path := tmp_path / TEST_INPUT_FILE).touch()
    ts_path.write_text(get_basic_tree_script())
    return Path(str(tmp_path))


@pytest.fixture
def mock_nested_tree(tmp_path):
    (src_dir := tmp_path / 'src').mkdir()
    (main_dir := src_dir / 'main').mkdir()
    (main_dir / 'SourceClass.java').touch()
    (ts_path := tmp_path / TEST_INPUT_FILE).touch()
    ts_path.write_text(get_nested_tree_script())
    return Path(str(tmp_path))


@pytest.fixture
def mock_empty_dirs_tree(tmp_path):
    (my_dirs := tmp_path / 'empty_dirs/').mkdir()
    for n in range(1, 4): # Create Numbered Empty Dirs
        (my_dirs / f'dir{n}').mkdir()
    (ts_path := tmp_path / TEST_INPUT_FILE).touch()
    ts_path.write_text(get_empty_dirs_tree_script())
    return Path(str(tmp_path))


@pytest.fixture
def mock_hidden_tree(tmp_path):
    (github_dir := tmp_path / '.github').mkdir()
    (github_dir / 'dependabot.yml').touch()
    (workflows_dir := github_dir / 'workflows').mkdir()
    (workflows_dir / 'ci.yml').touch()
    (tmp_path / '.hidden.txt').touch()
    (ts_path := tmp_path / TEST_INPUT_FILE).touch()
    ts_path.write_text(get_hidden_tree_script())
    return Path(str(tmp_path))


def get_input_data(
    input_tree_name: str,
    control_mode: ControlMode,
    move_files: bool = False,
    is_trim: bool = False,
    verbosity: int = 1,
) -> InputData:
    return InputData(
        tree_input=get_treescript_input_sample(input_tree_name),
        data_dir=None,
        trim_tree=is_trim,
        move_files=move_files,
        control_mode=control_mode,
        verbosity_level=verbosity,
    )


def input_data_with_dir(
    input_tree_name: str,
    data_dir: str,
    control_mode: ControlMode,
    move_files: bool,
    is_trim: bool = False,
    verbosity: int = 1,
) -> tuple[InputData, TemporaryDirectory]:
    tmp_dir = TemporaryDirectory()
    (data_dir_path := Path(tmp_dir.name) / data_dir).mkdir(parents=True)
    return InputData(
        tree_input=get_treescript_input_sample(input_tree_name),
        data_dir=data_dir_path,
        trim_tree=is_trim,
        move_files=move_files,
        control_mode=control_mode,
        verbosity_level=verbosity,
    ), tmp_dir
