""" Testing Build Validation Methods.
"""
import pytest
from pathlib import Path

from test.treescript_builder.tree.conftest import generate_simple_tree, generate_gradle_module_tree, \
    generate_python_package_tree, generate_complex_tree, generate_gradle_module_tree_with_data, \
    generate_invalid_tree_line_1, generate_invalid_tree_line_2, generate_simple_tree_instructions, \
    generate_gradle_module_tree_instructions, generate_complex_tree_instructions, \
    generate_gradle_module_tree_instructions_with_data
from treescript_builder.data.data_directory import DataDirectory
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.data.tree_data import TreeData
from treescript_builder.tree.build_validation import validate_build


def test_validate_build_simple_tree_returns_data():
    assert validate_build(generate_simple_tree(), None) == tuple(
        generate_simple_tree_instructions()
    )


def test_validate_build_two_nested_dirs_returns_one_instruction():
    def generate_two_nested_dirs():
        yield TreeData(1, 0, True, 'module1', '')
        yield TreeData(2, 1, True, 'src', '')
    assert validate_build(generate_two_nested_dirs(), None) == (
        InstructionData(True, Path('module1/src/'), None),
    )


def test_validate_build_three_nested_dirs_returns_one_instruction():
    def generate_three_nested_dirs():
        yield TreeData(1, 0, True, 'module1', '')
        yield TreeData(2, 1, True, 'src', '')
        yield TreeData(5, 2, True, 'main', '')
    assert validate_build(generate_three_nested_dirs(), None) == (
        InstructionData(True, Path('module1/src/main'), None),
    )


def test_validate_build_gradle_module_tree_returns_data():
    assert validate_build(generate_gradle_module_tree(), None) == tuple(
        generate_gradle_module_tree_instructions()
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
    with pytest.raises(SystemExit):
        validate_build(generator, None)


def test_validate_build_with_data_dir_simple_tree_returns_data():
    data_dir_path = Path('.ftb/data/')
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        assert validate_build(generate_simple_tree(), data_dir_path) == (
            InstructionData(True, Path('src/'), None),
            InstructionData(False, Path('src/data.txt'), None),
        )


def test_validate_build_with_data_dir_gradle_module_tree_returns_data():
    data_dir_path = Path('.ftb/data/')
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(DataDirectory, 'validate_build', lambda _, x: data_dir_path / x.data_label)
        assert validate_build(generate_gradle_module_tree_with_data(), data_dir_path) == tuple(
            generate_gradle_module_tree_instructions_with_data()
        )


def test_validate_build_with_data_dir_complex_tree_returns_data():
    data_dir_path = Path('.ftb/data/')
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        assert validate_build(generate_complex_tree(), data_dir_path) == tuple(
            generate_complex_tree_instructions()
        )


@pytest.mark.parametrize(
    'generator',
    [
        generate_invalid_tree_line_1(),
        generate_invalid_tree_line_2(),
    ]
)
def test_validate_build_with_data_dir_invalid_tree_raises_exit(generator):
    data_dir_path = Path('.ftb/data/')
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        with pytest.raises(SystemExit):
            validate_build(generator, data_dir_path)
