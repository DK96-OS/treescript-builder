""" Testing Path Operations Module Method.
"""
from pathlib import Path

import pytest

from test.conftest import create_data_tree, DATA_TREE_DATA_DIR_NAME, DATA_TREE_DATA_FILE_NAME, DATA_TREE_TARGET_FILE_NAME, \
    DATA_TREE_TARGET_DIR_NAME, DATA_TREE_DATA_FILE_CONTENTS, DATA_TREE_TARGET_FILE_CONTENTS
from test.treescript_builder.conftest import raise_exception
from treescript_builder.operations import path_operations
from treescript_builder.operations.path_operations import make_dir_exist, get_text_merge_method, get_write_operation


def test_make_dir_exist_empty_path_returns_true(mock_basic_tree):
    test_input = Path("")
    assert test_input.exists() # This returns true, so the operation does not need to proceed
    assert make_dir_exist(test_input)


@pytest.mark.parametrize(
    'dir_path', [
        "src/",
        "src/src/",
        "src/src/src/",
        "src/java/"
    ]
)
def test_make_dir_exist_src_already_exists_returns_true(mock_basic_tree, dir_path):
    test_input = mock_basic_tree / dir_path
    assert make_dir_exist(test_input)


def test_make_dir_exist_mock_mkdir_raises_oserror_returns_false(mock_basic_tree):
    test_input = mock_basic_tree / "src/java/"
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'mkdir', lambda _,**kwargs: raise_exception('oserror'))
        assert not make_dir_exist(test_input)


@pytest.mark.parametrize(
    'move_files, is_prepend, expected_method', [
        (False, False, path_operations._append_copy),
        (True, False, path_operations._append_move),
        (False, True, path_operations._prepend_copy),
        (True, True, path_operations._prepend_move),
    ]
)
def test_get_text_merge_method_parametrized_returns_expected_method(move_files, is_prepend, expected_method):
    assert expected_method == get_text_merge_method(move_file=move_files, prepend=is_prepend)


@pytest.mark.parametrize(
    'move_files, overwrite, exact, expected_method', [
        (False, False, False, path_operations._try_copy),
        (False, True, False, path_operations._ow_copy),
        (False, True, True, path_operations._ow_exact_copy),
        # Move Operations
        (True, False, False, path_operations._try_move),
        (True, True, False, path_operations._ow_move),
        (True, True, True, path_operations._ow_exact_move),
    ]
)
def test_get_write_operation_parametrized_returns_expected_method(move_files, overwrite, exact, expected_method):
    assert expected_method == get_write_operation(move_files, overwrite, exact)


def test_append_to_file_data_tree_copy_source_path_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=False)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    #
    assert get_text_merge_method(move_file=False, prepend=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_append_to_file_data_tree_initial_target_contents_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=True)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    assert get_text_merge_method(move_file=False, prepend=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_TARGET_FILE_CONTENTS + DATA_TREE_DATA_FILE_CONTENTS


def test_append_to_file_empty_target_file_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=False)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    target_path.unlink()
    target_path.touch()
    #
    assert get_text_merge_method(move_file=False, prepend=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_prepend_to_file_data_tree_initial_target_contents_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=True)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    #
    assert get_text_merge_method(move_file=False, prepend=True)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS + DATA_TREE_TARGET_FILE_CONTENTS


def test_prepend_to_file_empty_target_file_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=False)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    target_path.unlink()
    #
    assert get_text_merge_method(move_file=False, prepend=True)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_trywrite_data_tree_empty_target_file_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=False)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    #
    assert get_write_operation(move_file=False, overwrite=False, exact=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_trywrite_data_tree_no_target_file_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=False)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    target_path.unlink()
    #
    assert get_write_operation(move_file=False, overwrite=False, exact=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_trywrite_data_tree_initial_target_contents_copy_returns_false(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=True)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    #
    assert not get_write_operation(move_file=False, overwrite=False, exact=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_TARGET_FILE_CONTENTS # The File Contents are unaffected by the failed operation


def test_overwrite_file_data_tree_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=False)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    #
    assert get_write_operation(move_file=False, overwrite=True, exact=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_overwrite_file_data_tree_initial_target_contents_copy_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=True)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    #
    assert get_write_operation(move_file=False, overwrite=True, exact=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS


def test_overwrite_file_data_tree_no_target_file_returns_true(temp_cwd):
    create_data_tree(tempdir_path := Path(temp_cwd.name), initial_target_content=False)
    target_path = tempdir_path / DATA_TREE_TARGET_DIR_NAME / DATA_TREE_TARGET_FILE_NAME
    data_path = tempdir_path / DATA_TREE_DATA_DIR_NAME / DATA_TREE_DATA_FILE_NAME
    target_path.unlink()
    #
    assert get_write_operation(move_file=False, overwrite=True, exact=False)(target_path, data_path)
    #
    result = target_path.read_text()
    assert result == DATA_TREE_DATA_FILE_CONTENTS
