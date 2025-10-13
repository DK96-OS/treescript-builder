""" Test Fixtures & Data Providers.
"""
from pathlib import Path

import pytest

from treescript_builder.data.control_modes import WriteControlModes, TextMergeControlModes
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.line_reader import SPACE_CHARS


def raise_exception(name: str):
    """ Raise an Exception in a mock method.
 - Argument is lowercased before matching.

**Available Exceptions:**
 - OSError
 - IOError
 - SystemExit
 - ValueError
 - TypeError
 - BaseException

**Parameters:**
 - name (str): The name of the Exception to be raised during method execution.
    """
    match name.lower():
        case 'oserror':
            raise OSError
        case 'ioerror':
            raise IOError
        case 'systemexit':
            raise SystemExit
        case 'valueerror':
            raise ValueError
        case 'typeerror':
            raise TypeError
        case 'baseexception':
            raise BaseException


def create_depth(depth: int) -> str:
    """ Creates a string of space chars equivalent to the given depth.

**Parameters:**
 - depth (int): The amount of depth in the Tree Node Structure.

**Returns:**
 str - The String of a Space Char, of the required length.
	"""
    return SPACE_CHARS[0] * depth * 2


def get_control_mode_write(
    overwrite: bool = False,
    exact: bool = False,
    continue_build: bool = False,
    validate: bool = False,
) -> WriteControlModes:
    return WriteControlModes(
        overwrite=overwrite,
        exact_build=exact,
        continue_build=continue_build,
        validate=validate,
    )


def get_control_mode_text_merge(
    is_prepend: bool,
    continue_build: bool = False,
) -> TextMergeControlModes:
    return TextMergeControlModes(
        prepend_merge=is_prepend,
        continue_build=continue_build,
    )


@pytest.fixture
def control_trywrite():
    return WriteControlModes()


@pytest.fixture
def control_overwrite():
    return WriteControlModes(overwrite=True)


@pytest.fixture
def control_overwrite_exact():
    return WriteControlModes(overwrite=True, exact_build=True)


@pytest.fixture
def control_text_append():
    return TextMergeControlModes()


@pytest.fixture
def control_text_prepend():
    return TextMergeControlModes(prepend_merge=True)


def get_basic_data_tree_instructions() -> tuple[InstructionData, ...]:
    return (
        InstructionData(True, Path('src/'), None),
        InstructionData(False, Path('src/data.txt'), Path('data/dir/DataLabel')),
    )


def get_nested_tree_instructions() -> tuple[InstructionData, ...]:
    return (
        InstructionData(True, Path('src/main/'), None),
        InstructionData(False, Path('src/main/SourceClass.java'), None),
    )


def get_empty_dirs_tree_instructions() -> tuple[InstructionData, ...]:
    return (
        InstructionData(True, Path('empty_dirs/dir1/'), None),
        InstructionData(True, Path('empty_dirs/dir2/'), None),
        InstructionData(True, Path('empty_dirs/dir3/'), None),
    )


def get_hidden_tree_instructions() -> tuple[InstructionData, ...]:
    return (
        InstructionData(True, Path('.github/'), None),
        InstructionData(False, Path('.github/dependabot.yml'), None),
        InstructionData(True, Path('.github/workflows/'), None),
        InstructionData(False, Path('.github/workflows/ci.yml'), None),
        InstructionData(False, Path('.hidden.txt'), None),
    )
