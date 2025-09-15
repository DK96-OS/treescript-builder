""" Testing Path Operations Module Method.
"""
from pathlib import Path

import pytest

from test.conftest import mock_basic_tree
from treescript_builder.tree.path_operations import make_dir_exist, prepend_to_file, append_to_file, overwrite_file


def mock_mkdir_raise_oserror(*args, **kwargs):
    raise OSError


def test_make_dir_exist_empty_path_returns_true(mock_basic_tree):
    test_input = Path("")
    assert make_dir_exist(test_input)


def test_make_dir_exist_relative_src_path_returns_true(mock_basic_tree):
    test_input = Path("src/")
    assert make_dir_exist(test_input)


def test_make_dir_exist_src_already_exists_returns_true(mock_basic_tree):
    test_input = mock_basic_tree / "src/"
    assert make_dir_exist(test_input)


def test_make_dir_exist_nested_src_1_returns_true(mock_basic_tree):
    test_input = mock_basic_tree / "src/src/"
    assert make_dir_exist(test_input)


def test_make_dir_exist_nested_src_2_returns_true(mock_basic_tree):
    test_input = mock_basic_tree / "src/src/src/"
    assert make_dir_exist(test_input)


def test_make_dir_exist_nested_java_returns_true(mock_basic_tree):
    test_input = mock_basic_tree / "src/java/"
    assert make_dir_exist(test_input)


def test_make_dir_exist_other_dir_returns_true(mock_basic_tree):
    test_input = mock_basic_tree / "other_dir/"
    assert make_dir_exist(test_input)


def test_make_dir_exist_nested_java_dir_raises_oserror_returns_false(mock_basic_tree):
    test_input = mock_basic_tree / "src/java/"
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'mkdir', mock_mkdir_raise_oserror)
        assert not make_dir_exist(test_input)


def test_append_to_file(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    source_path = mock_data_tree / "data_dir" / "data_file.txt"
    assert append_to_file(target_path, source_path)
    #
    result = target_path.read_text()
    assert result == """Target File Contents.Data File Contents."""


def test_append_to_file_none_source_path_returns_true(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    assert append_to_file(target_path, None)
    #
    result = target_path.read_text()
    assert result == """Target File Contents."""


def test_append_to_file_empty_target_file(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    source_path = mock_data_tree / "data_dir" / "data_file.txt"
    #
    target_path.unlink()
    target_path.touch()
    #
    assert append_to_file(target_path, source_path)
    #
    result = target_path.read_text()
    assert result == """Data File Contents."""


def test_prepend_to_file(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    source_path = mock_data_tree / "data_dir" / "data_file.txt"
    assert prepend_to_file(target_path, source_path)
    #
    result = target_path.read_text()
    assert result == """Data File Contents.Target File Contents."""


def test_prepend_to_file_none_source_path_return_true(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    assert prepend_to_file(target_path, None)
    #
    result = target_path.read_text()
    assert result == """Target File Contents."""


def test_prepend_to_file_empty_target_file_returns_true(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    source_path = mock_data_tree / "data_dir" / "data_file.txt"
    #
    target_path.unlink()
    target_path.touch()
    #
    assert prepend_to_file(target_path, source_path)
    #
    result = target_path.read_text()
    assert result == """Data File Contents."""


def test_overwrite_file(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    source_path = mock_data_tree / "data_dir" / "data_file.txt"
    assert overwrite_file(target_path, source_path)
    #
    result = target_path.read_text()
    assert result == """Data File Contents."""


def test_overwrite_file_empty_source_(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    source_path = mock_data_tree / "data_dir" / "data_file.txt"
    assert overwrite_file(target_path, source_path)
    #
    result = target_path.read_text()
    assert result == """Data File Contents."""


def test_overwrite_file_empty_target_file_returns_true(mock_data_tree):
    target_path = mock_data_tree / "target_dir" / "target_file.txt"
    source_path = mock_data_tree / "data_dir" / "data_file.txt"
    #
    target_path.unlink()
    target_path.touch()
    #
    assert overwrite_file(target_path, source_path)
    #
    result = target_path.read_text()
    assert result == """Data File Contents."""
