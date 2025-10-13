""" Testing Input Package Method: validate_input_arguments.
"""
from pathlib import Path
import os

import pytest

from test.conftest import TS_INPUT_STR_1, input_data_with_dir, get_input_data, TEST_INPUT_FILE, TEST_DATA_DIR
from test.treescript_builder.conftest import get_control_mode_write, get_control_mode_text_merge
from treescript_builder.input import validate_input_arguments, InputData, file_validation

from test.treescript_builder.input.conftest import MockPathStat


def test_validate_input_arguments_returns_input_data():
    tree_input_data = 'src/\n  data.txt'
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: tree_input_data)
        #
        result = validate_input_arguments([TEST_INPUT_FILE])
        assert result is not None
        assert result.data_dir is None
        assert not result.trim_tree
        assert result.tree_input == tree_input_data


def test_validate_input_arguments_input_file_does_not_exist_raises_error():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        with pytest.raises(SystemExit):
            validate_input_arguments([TEST_INPUT_FILE])


def test_validate_input_arguments_input_file_is_empty_returns_input_no_data_dir():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: '')
        result = validate_input_arguments([TEST_INPUT_FILE])
        assert result is not None
        assert result.data_dir is None


def test_validate_input_arguments_input_file_is_empty_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: '')
        with pytest.raises(SystemExit, match=file_validation._FILE_VALIDATION_ERROR_MSG):
            validate_input_arguments([TEST_INPUT_FILE])


def test_validate_input_arguments_unknown_argument_raises_error():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        with pytest.raises(SystemExit):
            validate_input_arguments([TEST_INPUT_FILE, 'random-arg'])


def test_validate_input_arguments_sample_temp_dir(tmp_path: Path):
    (input_file := (tmp_path / TEST_INPUT_FILE)).touch()
    input_file.write_text(TS_INPUT_STR_1)
    os.chdir(tmp_path)
    #
    result: InputData = validate_input_arguments([TEST_INPUT_FILE])
    assert result.tree_input == TS_INPUT_STR_1
    assert result.data_dir is None
    assert not result.trim_tree
    
    result.text_mode
    result.control_mode
    result.move_files
    
    assert result.verbosity_level == 0


@pytest.mark.parametrize(
    "test_input, expected", [
        ([TEST_INPUT_FILE], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=0)),
        # Note: Cancel increases Verbosity to minimum 1
        ([TEST_INPUT_FILE, '-c'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=0)),
        ([TEST_INPUT_FILE, '-m'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=0)),
        ([TEST_INPUT_FILE, '-o'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=0)),
        ([TEST_INPUT_FILE, '-p'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=0)),
        # Reversed/Trim
        ([TEST_INPUT_FILE, '-cr'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), is_trim=True, verbosity=0)),
        ([TEST_INPUT_FILE, '-mr'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), is_trim=True, verbosity=0)),
        ([TEST_INPUT_FILE, '-or'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), is_trim=True, verbosity=0)),
        ([TEST_INPUT_FILE, '-pr'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), is_trim=True, verbosity=0)),
        # Verbosity Level
        ([TEST_INPUT_FILE, '-v'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=1)),
        ([TEST_INPUT_FILE, '-vv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=2)),
        # When Combined with CANCEL:
        ([TEST_INPUT_FILE, '-cv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=1)),
        ([TEST_INPUT_FILE, '-cvv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=2)),
    ]
)
def test_validate_input_arguments_temp_dir_ts_input_str_1_returns_data(
    test_input: list[str],
    expected: InputData,
    tmp_path: Path,
):
    (input_file := (tmp_path / TEST_INPUT_FILE)).touch()
    input_file.write_text(TS_INPUT_STR_1)
    os.chdir(tmp_path)
    # Object Comparison
    assert expected == validate_input_arguments(test_input)


@pytest.mark.parametrize(
    "test_input, expected", [
        ([TEST_INPUT_FILE, '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(overwrite=False, exact=False), move_files=False)),
        # Note: Cancel increases Verbosity to minimum 1.
        ([TEST_INPUT_FILE, '--data_dir', TEST_DATA_DIR, '-c'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False)),
        ([TEST_INPUT_FILE, '--data_dir', TEST_DATA_DIR, '-m'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=True)),
        ([TEST_INPUT_FILE, '--data_dir', TEST_DATA_DIR, '-o'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(overwrite=True,), move_files=False)),
        ([TEST_INPUT_FILE, '--data_dir', TEST_DATA_DIR, '-p'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=True), move_files=False)),
        # Reversed/Trim
        ([TEST_INPUT_FILE, '-cr', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, is_trim=True, verbosity=1)),
        ([TEST_INPUT_FILE, '-mr', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=True, is_trim=True)),
        ([TEST_INPUT_FILE, '-or', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, is_trim=True)),
        ([TEST_INPUT_FILE, '-pr', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=True), move_files=False, is_trim=True)),
        # Verbosity Level
        ([TEST_INPUT_FILE, '-v', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=1)),
        ([TEST_INPUT_FILE, '-vv', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=2)),
        ([TEST_INPUT_FILE, '-vvv', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=2)),
        # Combined with CANCEL:
        ([TEST_INPUT_FILE, '-cv', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=1)),
        ([TEST_INPUT_FILE, '-cvv', '--data_dir', TEST_DATA_DIR], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=2)),
    ]
)
def test_validate_input_arguments_temp_dir_ts_input_str_1_with_data_dir_returns_data(
    test_input: list[str],
    expected: get_input_data,
    tmp_path: Path,
):
    (input_file := (tmp_path / TEST_INPUT_FILE)).touch()
    input_file.write_text(TS_INPUT_STR_1)
    (tmp_path / TEST_DATA_DIR).mkdir(parents=True)
    os.chdir(tmp_path)
    # Object Comparison
    assert expected == validate_input_arguments(test_input)
