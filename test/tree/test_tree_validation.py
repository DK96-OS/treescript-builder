"""Testing Tree Validation Methods.
"""
from input.tree_data import TreeData
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

def generate_complex_tree():
    """
    Complex Tree: an example Gradle-Java project.
    """
    yield TreeData(1, 0, True, '.github', '')
    yield TreeData(2, 1, True, 'workflows', '')
    yield TreeData(3, 0, True, 'module1', '')
    yield TreeData(4, 1, False, 'build.gradle', '')
    yield TreeData(5, 1, True, 'src', '')
    yield TreeData(6, 2, True, 'main', '')
    yield TreeData(7, 3, True, 'java', '')
    yield TreeData(8, 4, True, 'com', '')
    yield TreeData(9, 5, True, 'example', '')
    yield TreeData(10, 6, False, 'Main.java', '')
    yield TreeData(11, 2, True, 'test', '')
    yield TreeData(12, 3, True, 'java', '')
    yield TreeData(13, 4, True, 'com', '')
    yield TreeData(14, 5, True, 'example', '')
    yield TreeData(15, 6, False, 'MainTest.java', '')
    yield TreeData(16, 0, False, 'README.md', '')
    yield TreeData(17, 0, False, 'build.gradle', '')
    yield TreeData(18, 0, False, 'settings.gradle', '')


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


def test_validate_tree_simple_tree_returns_data():
    assert validate_tree(generate_simple_tree()) == (
        InstructionData(True, Path('src/'), None),
        InstructionData(False, Path('src/data.txt'), None),
    )


def test_validate_tree_complex_tree_returns_data():
    assert validate_tree(generate_simple_tree()) == (
        InstructionData(True, Path('.github/workflows/'), None),
        InstructionData(True, Path('module1/'), None),
        InstructionData(False, Path('module1/build.gradle'), None),
        InstructionData(True, Path('module1/src/main/java/com/example/'), None),
        InstructionData(False, Path('module1/src/main/java/com/example/Main.java'), None),
        InstructionData(True, Path('module1/src/test/java/com/example/'), None),
        InstructionData(False, Path('module1/src/test/java/com/example/MainTest.java'), None),
        InstructionData(False, Path('README.md'), None),
        InstructionData(False, Path('build.gradle'), None),
        InstructionData(False, Path('settings.gradle'), None),
    )


@pytest.mark.parametrize(
    'generator',
    [
        generate_invalid_tree_line_1(),
        generate_invalid_tree_line_2(),
    ]
)
def test_validate_tree_invalid_tree_raises_exit(generator):
    try:
        validate_tree(generator)
        assert False
    except SystemExit as e:
        assert True


def test_validate_with_data_dir_simple_tree_returns_data():
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
def test_validate_with_data_dir_invalid_tree_raises_exit(generator):
    data_dir = pytest.MonkeyPatch()
    try:
        validate_with_data_dir(generator, data_dir)
        assert False
    except SystemExit as e:
        assert True
