""" Testing the Tree Module Init Build Tree Method.
"""
from re import escape

import pytest

from test.conftest import get_input_data, input_data_with_dir
from test.treescript_builder.conftest import get_nested_tree_instructions, get_control_mode_write, \
    get_hidden_tree_instructions, get_empty_dirs_tree_instructions
from test.treescript_builder.tree.conftest import generate_simple_tree_instructions
from treescript_builder.tree import validate_tree


@pytest.mark.parametrize(
    "input_data, expected_instructions", [
        (get_input_data('basic', get_control_mode_write()), tuple(generate_simple_tree_instructions())),
        (get_input_data('nested', get_control_mode_write()), get_nested_tree_instructions()),
        (get_input_data('hidden', get_control_mode_write()), get_hidden_tree_instructions()),
        (get_input_data('empty_dirs', get_control_mode_write()), get_empty_dirs_tree_instructions()),
    ]
)
def test_validate_tree_trywrite_returns_data(input_data, expected_instructions):
    assert expected_instructions == validate_tree(input_data)


@pytest.mark.parametrize(
    "input_data_and_dir", [
        input_data_with_dir('basic+data', 'data/dir', get_control_mode_write(), False),
    ]
)
def test_validate_tree_with_data_trywrite_data_file_does_not_exist_raises_exit(input_data_and_dir: tuple):
    with pytest.raises(SystemExit, match=escape('Label (DataLabel) not found in DataDirectory on Line: 2')):
        validate_tree(input_data_and_dir[0])


@pytest.mark.parametrize(
    "input_data, expected_instructions", [
        (get_input_data('basic', get_control_mode_write(overwrite=True)), tuple(generate_simple_tree_instructions())),
        (get_input_data('nested', get_control_mode_write(overwrite=True)), get_nested_tree_instructions()),
        (get_input_data('hidden', get_control_mode_write(overwrite=True)), get_hidden_tree_instructions()),
        (get_input_data('empty_dirs', get_control_mode_write(overwrite=True)), get_empty_dirs_tree_instructions()),
    ]
)
def test_validate_tree_overwrite_returns_data(input_data, expected_instructions):
    assert expected_instructions == validate_tree(input_data)


@pytest.mark.parametrize(
    "input_data, expected_instructions", [
        (get_input_data('basic', get_control_mode_write(overwrite=True, exact=True)), tuple(generate_simple_tree_instructions())),
        (get_input_data('nested', get_control_mode_write(overwrite=True, exact=True)), get_nested_tree_instructions()),
        (get_input_data('hidden', get_control_mode_write(overwrite=True, exact=True)), get_hidden_tree_instructions()),
        (get_input_data('empty_dirs', get_control_mode_write(overwrite=True, exact=True)), get_empty_dirs_tree_instructions()),
    ]
)
def test_validate_tree_overwrite_exact_returns_data(input_data, expected_instructions):
    assert expected_instructions == validate_tree(input_data)


@pytest.mark.parametrize(
    "input_data, expected_instructions", [
        (get_input_data('basic', get_control_mode_write(overwrite=True, exact=True, validate=True)), tuple(generate_simple_tree_instructions())),
        (get_input_data('nested', get_control_mode_write(overwrite=True, exact=True, validate=True)), get_nested_tree_instructions()),
        (get_input_data('hidden', get_control_mode_write(overwrite=True, exact=True, validate=True)), get_hidden_tree_instructions()),
        (get_input_data('empty_dirs', get_control_mode_write(overwrite=True, exact=True, validate=True)), get_empty_dirs_tree_instructions()),
    ]
)
def test_validate_tree_overwrite_exact_validate_returns_data(input_data, expected_instructions):
    assert expected_instructions == validate_tree(input_data)


@pytest.mark.parametrize(
    "input_data, expected_instructions", [
        (get_input_data('basic', get_control_mode_write(validate=True)), tuple(generate_simple_tree_instructions())),
        (get_input_data('nested', get_control_mode_write(validate=True)), get_nested_tree_instructions()),
        (get_input_data('hidden', get_control_mode_write(validate=True)), get_hidden_tree_instructions()),
        (get_input_data('empty_dirs', get_control_mode_write(validate=True)), get_empty_dirs_tree_instructions()),
    ]
)
def test_validate_tree_trywrite_validate_returns_data(input_data, expected_instructions):
    assert expected_instructions == validate_tree(input_data)


@pytest.mark.parametrize(
    "input_data_and_dir", [
        input_data_with_dir('basic+data', 'data/dir', get_control_mode_write(validate=True), False),
    ]
)
def test_validate_tree_with_data_validate_data_file_does_not_exist_raises_exit(input_data_and_dir: tuple):
    with pytest.raises(SystemExit, match=escape('Label (DataLabel) not found in DataDirectory on Line: 2')):
        validate_tree(input_data_and_dir[0])


@pytest.mark.parametrize(
    "input_data, expected_instructions", [
        (get_input_data('basic', get_control_mode_write(continue_build=True)), tuple(generate_simple_tree_instructions())),
        (get_input_data('nested', get_control_mode_write(continue_build=True)), get_nested_tree_instructions()),
        (get_input_data('hidden', get_control_mode_write(continue_build=True)), get_hidden_tree_instructions()),
        (get_input_data('empty_dirs', get_control_mode_write(continue_build=True)), get_empty_dirs_tree_instructions()),
    ]
)
def test_validate_tree_trywrite_continue_build_returns_data(input_data, expected_instructions):
    assert expected_instructions == validate_tree(input_data)


@pytest.mark.parametrize(
    "input_data_and_dir", [
        input_data_with_dir('basic+data', 'data/dir', get_control_mode_write(continue_build=True), False),
    ]
)
def test_validate_tree_with_data_continue_build_returns_data(input_data_and_dir: tuple):
    with pytest.raises(SystemExit, match=escape('Label (DataLabel) not found in DataDirectory on Line: 2')):
        validate_tree(input_data_and_dir[0])
