"""Testing Build Validation Methods.
"""
import pytest
from pathlib import Path

from input.data_directory import DataDirectory
from tree.instruction_data import InstructionData
from tree.build_validation import validate_build

from test.tree.tree_generators import *


def test_validate_build_simple_tree_returns_data():
    assert validate_build(generate_simple_tree(), None) == (
        InstructionData(True, Path('src/'), None),
        InstructionData(False, Path('src/data.txt'), None),
    )


def test_validate_build_gradle_module_tree_returns_data():
    assert validate_build(generate_gradle_module_tree(), None) == (
        InstructionData(True, Path('module1/'), None),
        InstructionData(False, Path('module1/build.gradle'), None),
        InstructionData(True, Path('module1/src/main/java/'), None),
        InstructionData(True, Path('module1/src/test/java/'), None),
    )


def test_validate_build_python_package_tree_returns_data():
    assert validate_build(generate_python_package_tree(), None) == (
        InstructionData(True, Path('package_name/'), None),
        InstructionData(False, Path('package_name/__init__.py'), None),
        InstructionData(False, Path('package_name/internal_module.py'), None),
    )


def test_validate_build_complex_tree_returns_data():
    assert validate_build(generate_complex_tree(), None) == (
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
def test_validate_build_invalid_tree_raises_exit(generator):
    try:
        validate_build(generator, None)
        assert False
    except SystemExit as e:
        assert True


def test_validate_build_with_data_dir_simple_tree_returns_data():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        #
        assert validate_build(generate_simple_tree(), data_dir) == (
            InstructionData(True, Path('src/'), None),
            InstructionData(False, Path('src/data.txt'), None),
        )


def test_validate_build_with_data_dir_gradle_module_tree_returns_data():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        assert validate_build(generate_gradle_module_tree(), data_dir) == (
            InstructionData(True, Path('module1/'), None),
            InstructionData(False, Path('module1/build.gradle'), Path('.ftb/data/gbuild_module1')),
            InstructionData(True, Path('module1/src/main/java/'), None),
            InstructionData(True, Path('module1/src/test/java/'), None),
        )


def test_validate_build_with_data_dir_complex_tree_returns_data():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        assert validate_build(generate_complex_tree(), data_dir) == (
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
def test_validate_build_with_data_dir_invalid_tree_raises_exit(generator):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        try:
            validate_build(generator, data_dir)
            assert False
        except SystemExit as e:
            assert True
