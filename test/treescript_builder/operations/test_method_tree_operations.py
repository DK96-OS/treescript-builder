""" Testing the Operations Package High Level Method Tree Operations.
"""
from os import chdir
from pathlib import Path

import pytest

from test.conftest import DATA_TREE_DATA_DIR_NAME, input_data_with_dir, DATA_TREE_TARGET_DIR_NAME, \
    DATA_TREE_TARGET_FILE_NAME, DATA_TREE_DATA_FILE_NAME, DATA_TREE_DATA_FILE_CONTENTS, get_input_data
from test.treescript_builder.conftest import get_control_mode_write, get_control_mode_text_merge
from treescript_builder.operations import tree_operations
from treescript_builder.tree import data_directory


@pytest.mark.parametrize(
    'move_files, verbosity, expected_result,', [
        (False, 0, ''),
        (False, 1, 'WRITE:\nAll File Operations Succeeded.'),
        (False, 2, 'WRITE:\nPass: src/\nPass: src/data.txt\nAll File Operations Succeeded.'),
        #
        (True, 0, ''),
        (True, 1, 'WRITE:\nAll File Operations Succeeded.'),
        (True, 2, 'WRITE:\nPass: src/\nPass: src/data.txt\nAll File Operations Succeeded.'),
    ]
)
def test_tree_operations_build_basic_tree_empty_tempdir_returns_results(move_files, verbosity, expected_result):
    input_data, temp_dir = input_data_with_dir(
        'basic',
        DATA_TREE_DATA_DIR_NAME,
        get_control_mode_write(),
        move_files=move_files,
        is_trim=False,
        verbosity=verbosity,
    )
    chdir(Path(temp_dir.name))
    assert expected_result == tree_operations(input_data)


@pytest.mark.parametrize(
    'move_files, verbosity,', [
        (False, 2, ),
        (True, 2, ),
    ]
)
def test_tree_operations_build_data_tree_missing_datalabel_raises_exit(move_files, verbosity):
    input_data, temp_dir = input_data_with_dir(
        'data_tree',
        DATA_TREE_DATA_DIR_NAME,
        get_control_mode_write(),
        move_files=move_files,
        is_trim=False,
        verbosity=verbosity,
    )
    chdir(Path(temp_dir.name))
    with pytest.raises(SystemExit, match=data_directory._DATA_LABEL_NOT_FOUND_MSG):
        tree_operations(input_data)


@pytest.mark.parametrize(
    'move_files, verbosity, expected_result,', [
        (False, 0, ''),
        (False, 1, 'WRITE:\nAll File Operations Succeeded.'),
        (False, 2, f'WRITE:\nPass: {DATA_TREE_TARGET_DIR_NAME}/\nPass: {DATA_TREE_TARGET_DIR_NAME}/{DATA_TREE_TARGET_FILE_NAME}\nAll File Operations Succeeded.'),
        #
        (True, 0, ''),
        (True, 1, 'WRITE:\nAll File Operations Succeeded.'),
        (True, 2, f'WRITE:\nPass: {DATA_TREE_TARGET_DIR_NAME}/\nPass: {DATA_TREE_TARGET_DIR_NAME}/{DATA_TREE_TARGET_FILE_NAME}\nAll File Operations Succeeded.'),
    ]
)
def test_tree_operations_build_data_tree_datadir_prepared_returns_results(move_files, verbosity, expected_result):
    input_data, temp_dir = input_data_with_dir(
        'data_tree',
        DATA_TREE_DATA_DIR_NAME,
        get_control_mode_write(),
        move_files=move_files,
        is_trim=False,
        verbosity=verbosity,
    )
    chdir(tempdir_path := Path(temp_dir.name))
    (datafile := tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME).touch()
    datafile.write_text(DATA_TREE_DATA_FILE_CONTENTS)
    assert expected_result == tree_operations(input_data)
    # Ensure file contents were written
    targetfile_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    assert DATA_TREE_DATA_FILE_CONTENTS == targetfile_path.read_text()


@pytest.mark.parametrize(
    'move_files, control_mode, verbosity, ',[
        (False, get_control_mode_write(), 2, ),
        (False, get_control_mode_write(True), 2, ),
        (False, get_control_mode_write(True, True), 2, ),
        (True, get_control_mode_write(), 2, ),
        (True, get_control_mode_write(True), 2, ),
        (True, get_control_mode_write(True, True), 2, ),
        #
        (False, get_control_mode_text_merge(False), 2, ),
        (False, get_control_mode_text_merge(True), 2, ),
        (True, get_control_mode_text_merge(False), 2, ),
        (True, get_control_mode_text_merge(True), 2, ),
    ]
)
def test_tree_operations_trim_basic_tree_with_data_but_empty_tempdir_raises_exit(move_files, control_mode, verbosity):
    input_data = get_input_data('basic+data', control_mode, move_files, is_trim=True, verbosity=verbosity)
    with pytest.raises(SystemExit, match=data_directory._DATA_DIR_NOT_PROVIDED_FOR_DATA_LABEL_MSG):
        tree_operations(input_data)


@pytest.mark.parametrize(
    'move_files, control_mode, verbosity, ',[
        (False, get_control_mode_write(), 2, ),
        (False, get_control_mode_write(True), 2, ),
        (False, get_control_mode_write(True, True), 2, ),
        (True, get_control_mode_write(), 2, ),
        (True, get_control_mode_write(True), 2, ),
        (True, get_control_mode_write(True, True), 2, ),
        #
        (False, get_control_mode_text_merge(False), 2, ),
        (False, get_control_mode_text_merge(True), 2, ),
        (True, get_control_mode_text_merge(False), 2, ),
        (True, get_control_mode_text_merge(True), 2, ),
    ]
)
def test_tree_operations_trim_data_tree_empty_tempdir_raises_exit(move_files, control_mode, verbosity):
    input_data = get_input_data('data_tree', control_mode, move_files, is_trim=True, verbosity=verbosity)
    with pytest.raises(SystemExit, match=data_directory._DATA_DIR_NOT_PROVIDED_FOR_DATA_LABEL_MSG):
        tree_operations(input_data)
