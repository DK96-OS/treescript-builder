"""Testing Tree Validation Methods.
"""
import pytest
from pathlib import Path
    
from input.line_reader import read_input_tree
from tree.instruction_data import InstructionData
from tree.tree_validation import validate_tree, validate_with_data_dir


def generate_simple_tree():
    """
    Simple Tree: a Directory and a File in that Directory.
    """
    return read_input_tree("src/\n  data.txt")


def generate_invalid_tree_line_1():
    """
    The First TreeData generated has a depth that is inconsistent with tree state.
    """
    return read_input_tree("  src/\n")


def generate_invalid_tree_line_2():
    """
    The Second TreeData generated has a depth that is inconsistent with tree state.
    """
    return read_input_tree("src/\n    data.txt")


def test_validate_tree_simple_tree():
    assert validate_tree(generate_simple_tree()) == (
        InstructionData(True, Path('src/'), None),
        InstructionData(False, Path('src/data.txt'), None),
    )


@pytest.mark.parametrize(
    'generator',
    [
        generate_invalid_tree_line_1(),
        generate_invalid_tree_line_2(),
    ]
)
def test_validate_tree_invalid_tree(generator):
    """
    """
    try:
        validate_tree(generator)
        assert False
    except SystemExit as e:
        assert True


def test_validate_with_data_dir_simple_tree():
    data_dir = pytest.MonkeyPatch()
    assert validate_with_data_dir(generate_simple_tree(), data_dir) == (
        InstructionData(True, Path('src/'), None),
        InstructionData(False, Path('src/data.txt'), None),
    )


@pytest.mark.parametrize(
    'generator',
    [
        generate_invalid_tree_line_1(),
        generate_invalid_tree_line_2(),
    ]
)
def test_validate_with_data_dir_invalid_tree(generator):
    """
    """
    data_dir = pytest.MonkeyPatch()
    try:
        validate_with_data_dir(generator, data_dir)
        assert False
    except SystemExit as e:
        assert True
