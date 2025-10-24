"""Testing Tree Validation Methods.
"""
from pathlib import Path

import pytest

from test.treescript_builder.tree.conftest import generate_simple_tree, generate_gradle_module_tree, \
    generate_python_package_tree, generate_complex_tree, generate_gradle_module_tree_with_data, \
    generate_invalid_tree_line_1, generate_invalid_tree_line_2
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.trim_validation import validate_trim


_DATA_DIR_PATH = Path('.ftb/data/')


def test_validate_trim_simple_tree_returns_data():
    assert validate_trim(generate_simple_tree(), None, move_files=False) == (
        InstructionData(False, Path('src/data.txt'), None),
    )


def test_validate_trim_simple_tree_move_files_returns_data():
    assert validate_trim(generate_simple_tree(), None, move_files=True) == (
        InstructionData(False, Path('src/data.txt'), None),
        InstructionData(True, Path('src/'), None),
    )


def test_validate_trim_gradle_module_tree_returns_data():
    assert validate_trim(generate_gradle_module_tree(), None) == (
        InstructionData(False, Path('module1/build.gradle'), None),
    )


def test_validate_trim_gradle_module_tree_move_files_returns_data():
    assert validate_trim(generate_gradle_module_tree(), None, move_files=True) == (
        InstructionData(False, Path('module1/build.gradle'), None),
        InstructionData(True, Path('module1/src/main/java/'), None),
        InstructionData(True, Path('module1/src/main/'), None),
        InstructionData(True, Path('module1/src/test/java/'), None),
        InstructionData(True, Path('module1/src/test/'), None),
        InstructionData(True, Path('module1/src/'), None),
        InstructionData(True, Path('module1/'), None),
    )


def test_validate_trim_python_package_tree_returns_data():
    assert validate_trim(generate_python_package_tree(), None) == (
        InstructionData(False, Path('package_name/__init__.py'), None),
        InstructionData(False, Path('package_name/internal_module.py'), None),
    )


def test_validate_trim_python_package_tree_move_files_returns_data():
    assert validate_trim(generate_python_package_tree(), None, move_files=True) == (
        InstructionData(False, Path('package_name/__init__.py'), None),
        InstructionData(False, Path('package_name/internal_module.py'), None),
        InstructionData(True, Path('package_name/'), None),
    )


def test_validate_trim_complex_tree_returns_data():
    assert validate_trim(generate_complex_tree(), None) == (
        InstructionData(False, Path('module1/build.gradle'), None),
        InstructionData(False, Path('module1/src/main/java/com/example/Main.java'), None),
        InstructionData(False, Path('module1/src/test/java/com/example/MainTest.java'), None),
        InstructionData(False, Path('README.md'), None),
        InstructionData(False, Path('build.gradle'), None),
        InstructionData(False, Path('settings.gradle'), None),
    )


def test_validate_trim_complex_tree_move_files_returns_data():
    assert validate_trim(generate_complex_tree(), None, move_files=True) == (
        InstructionData(True, Path('.github/workflows/'), None),
        InstructionData(True, Path('.github/'), None),
        InstructionData(False, Path('module1/build.gradle'), None),
        InstructionData(False, Path('module1/src/main/java/com/example/Main.java'), None),
        InstructionData(True, Path('module1/src/main/java/com/example/'), None),
        InstructionData(True, Path('module1/src/main/java/com/'), None),
        InstructionData(True, Path('module1/src/main/java/'), None),
        InstructionData(True, Path('module1/src/main/'), None),
        InstructionData(False, Path('module1/src/test/java/com/example/MainTest.java'), None),
        InstructionData(True, Path('module1/src/test/java/com/example/'), None),
        InstructionData(True, Path('module1/src/test/java/com/'), None),
        InstructionData(True, Path('module1/src/test/java/'), None),
        InstructionData(True, Path('module1/src/test/'), None),
        InstructionData(True, Path('module1/src/'), None),
        InstructionData(True, Path('module1/'), None),
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
def test_validate_trim_invalid_tree_raises_exit(generator):
    with pytest.raises(SystemExit):
        validate_trim(generator, None)


@pytest.mark.parametrize(
    'move_files, expected_instruction_tuple', [
        (False, (InstructionData(False, Path('src/data.txt'), None),)),
        (True, (InstructionData(False, Path('src/data.txt'), None), InstructionData(True, Path('src/'), None),)),
    ]
)
def test_validate_trim_with_data_dir_simple_tree_returns_data(move_files, expected_instruction_tuple):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        assert expected_instruction_tuple == validate_trim(generate_simple_tree(), _DATA_DIR_PATH, move_files=move_files)


@pytest.mark.parametrize(
    'move_files, expected_instruction_tuple', [
        (False, (
            InstructionData(False, Path('module1/build.gradle'), Path('.ftb/data/gbuild_module1')),
        )),
        (True, (
            InstructionData(False, Path('module1/build.gradle'), Path('.ftb/data/gbuild_module1')),
            InstructionData(True, Path('module1/src/main/java/'), None),
            InstructionData(True, Path('module1/src/main/'), None),
            InstructionData(True, Path('module1/src/test/java/'), None),
            InstructionData(True, Path('module1/src/test/'), None),
            InstructionData(True, Path('module1/src/'), None),
            InstructionData(True, Path('module1/'), None),
        )),
    ]
)
def test_validate_trim_with_data_dir_gradle_module_tree_returns_data(move_files, expected_instruction_tuple):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        assert expected_instruction_tuple == validate_trim(generate_gradle_module_tree_with_data(), _DATA_DIR_PATH, move_files=move_files)


@pytest.mark.parametrize(
    'move_files, expected_instruction_tuple', [
        (False, (
            InstructionData(False, Path('module1/build.gradle'), None),
            InstructionData(False, Path('module1/src/main/java/com/example/Main.java'), None),
            InstructionData(False, Path('module1/src/test/java/com/example/MainTest.java'), None),
            InstructionData(False, Path('README.md'), None),
            InstructionData(False, Path('build.gradle'), None),
            InstructionData(False, Path('settings.gradle'), None),
        )),
        (True, (
            InstructionData(True, Path('.github/workflows/'), None),
            InstructionData(True, Path('.github/'), None),
            InstructionData(False, Path('module1/build.gradle'), None),
            InstructionData(False, Path('module1/src/main/java/com/example/Main.java'), None),
            InstructionData(True, Path('module1/src/main/java/com/example/'), None),
            InstructionData(True, Path('module1/src/main/java/com/'), None),
            InstructionData(True, Path('module1/src/main/java/'), None),
            InstructionData(True, Path('module1/src/main/'), None),
            InstructionData(False, Path('module1/src/test/java/com/example/MainTest.java'), None),
            InstructionData(True, Path('module1/src/test/java/com/example/'), None),
            InstructionData(True, Path('module1/src/test/java/com/'), None),
            InstructionData(True, Path('module1/src/test/java/'), None),
            InstructionData(True, Path('module1/src/test/'), None),
            InstructionData(True, Path('module1/src/'), None),
            InstructionData(True, Path('module1/'), None),
            InstructionData(False, Path('README.md'), None),
            InstructionData(False, Path('build.gradle'), None),
            InstructionData(False, Path('settings.gradle'), None),
        )),
    ]
)
def test_validate_trim_with_data_dir_complex_tree_returns_data(move_files, expected_instruction_tuple):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        assert expected_instruction_tuple == validate_trim(generate_complex_tree(), _DATA_DIR_PATH, move_files=move_files)


@pytest.mark.parametrize(
    'generator',
    [
        generate_invalid_tree_line_1(),
        generate_invalid_tree_line_2(),
    ]
)
def test_validate_trim_with_data_dir_invalid_tree_raises_exit(generator):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        with pytest.raises(SystemExit):
            validate_trim(generator, _DATA_DIR_PATH)
