"""Testing Tree Validation Methods.
"""
import pytest
from pathlib import Path

from test.treescript_builder.tree.conftest import generate_simple_tree, generate_gradle_module_tree, \
    generate_python_package_tree, generate_complex_tree, generate_gradle_module_tree_with_data
from treescript_builder.data.data_directory import DataDirectory
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.trim_validation import validate_trim


def test_validate_trim_simple_tree_returns_data():
    assert validate_trim(generate_simple_tree(), None) == (
        InstructionData(False, Path('src/data.txt'), None),
        InstructionData(True, Path('src/'), None),
    )


def test_validate_trim_gradle_module_tree_returns_data():
    assert validate_trim(generate_gradle_module_tree(), None) == (
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
        InstructionData(True, Path('package_name/'), None),
    )


def test_validate_trim_complex_tree_returns_data():
    assert validate_trim(generate_complex_tree(), None) == (
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
    try:
        validate_trim(generator, None)
        assert False
    except SystemExit as e:
        assert True


def test_validate_trim_with_data_dir_simple_tree_returns_data():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        #
        assert validate_trim(generate_simple_tree(), data_dir) == (
            InstructionData(False, Path('src/data.txt'), None),
            InstructionData(True, Path('src/'), None),
        )


def test_validate_trim_with_data_dir_gradle_module_tree_returns_data():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        assert validate_trim(generate_gradle_module_tree_with_data(), data_dir) == (
            InstructionData(False, Path('module1/build.gradle'), Path('.ftb/data/gbuild_module1')),
            InstructionData(True, Path('module1/src/main/java/'), None),
            InstructionData(True, Path('module1/src/main/'), None),
            InstructionData(True, Path('module1/src/test/java/'), None),
            InstructionData(True, Path('module1/src/test/'), None),
            InstructionData(True, Path('module1/src/'), None),
            InstructionData(True, Path('module1/'), None),
        )


def test_validate_trim_with_data_dir_complex_tree_returns_data():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        assert validate_trim(generate_complex_tree(), data_dir) == (
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
def test_validate_trim_with_data_dir_invalid_tree_raises_exit(generator):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(Path('.ftb/data/'))
        try:
            validate_trim(generator, data_dir)
            assert False
        except SystemExit as e:
            assert True