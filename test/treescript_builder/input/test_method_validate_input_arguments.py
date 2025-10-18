""" Testing Input Package Method: validate_input_arguments.
"""
from os import chdir
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from test.conftest import TS_INPUT_STR_1, input_data_with_dir, get_input_data, TEST_INPUT_FILE, TEST_DATA_DIR
from test.treescript_builder.conftest import get_control_mode_write, get_control_mode_text_merge
from test.treescript_builder.input.conftest import MockPathStat

from treescript_builder.data.control_modes import WriteControlModes
from treescript_builder.input import validate_input_arguments, InputData, file_validation


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
        with pytest.raises(SystemExit, match=file_validation._FILE_DOES_NOT_EXIST_MSG):
            validate_input_arguments([TEST_INPUT_FILE])


def test_validate_input_arguments_input_file_larger_than_file_limit_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT + 1),)
        with pytest.raises(SystemExit, match=file_validation._FILE_SIZE_LIMIT_ERROR_MSG):
            validate_input_arguments([TEST_INPUT_FILE])


def test_validate_input_arguments_input_file_is_symlink_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT, is_symlink=True),)
        with pytest.raises(SystemExit, match=file_validation._FILE_SYMLINK_DISABLED_MSG):
            validate_input_arguments([TEST_INPUT_FILE])


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
        with pytest.raises(SystemExit, match='Unable to Parse Arguments.'):
            validate_input_arguments([TEST_INPUT_FILE, 'random-arg'])


def test_validate_input_arguments_sample_temp_dir(tmp_path: Path):
    (input_file := (tmp_path / TEST_INPUT_FILE)).touch()
    input_file.write_text(TS_INPUT_STR_1)
    chdir(tmp_path)
    #
    result: InputData = validate_input_arguments([TEST_INPUT_FILE])
    assert result.tree_input == TS_INPUT_STR_1
    assert result.data_dir is None
    assert not result.trim_tree
    assert not result.move_files
    assert result.verbosity_level == 0
    assert type(result.control_mode) == WriteControlModes


@pytest.mark.parametrize(
    "test_input, expected", [
        ([TEST_INPUT_FILE], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=0)),
        # Note: Cancel increases Verbosity to minimum 1
        ([TEST_INPUT_FILE, '-m'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=0, move_files=True),),
        # Trim
        ([TEST_INPUT_FILE, '-mt'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), move_files=True, is_trim=True, verbosity=0)),
        # Verbosity Level
        ([TEST_INPUT_FILE, '-v'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=1)),
        ([TEST_INPUT_FILE, '-vv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), verbosity=2)),
        # All Together
        ([TEST_INPUT_FILE, '-mv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), move_files=True, verbosity=1)),
        ([TEST_INPUT_FILE, '-mtv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), move_files=True, is_trim=True, verbosity=1)),
        ([TEST_INPUT_FILE, '-mvv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), move_files=True, verbosity=2)),
        ([TEST_INPUT_FILE, '-mtvv'], get_input_data(TEST_INPUT_FILE, get_control_mode_write(), move_files=True, is_trim=True, verbosity=2)),
    ]
)
def test_validate_input_arguments_temp_dir_ts_input_str_1_returns_data(
    test_input: list[str],
    expected: InputData,
    tmp_path: Path,
):
    (input_file := (tmp_path / TEST_INPUT_FILE)).touch()
    input_file.write_text(TS_INPUT_STR_1)
    chdir(tmp_path)
    # Object Comparison
    assert expected == validate_input_arguments(test_input)


@pytest.mark.parametrize(
    "test_input, expected", [
        ([TEST_INPUT_FILE, '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(overwrite=False, exact=False), move_files=False, verbosity=0)),
        # Note: Cancel increases Verbosity to minimum 1.
        ([TEST_INPUT_FILE, '-m', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=True, verbosity=0)),
        ([TEST_INPUT_FILE, '--overwrite', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(overwrite=True,), move_files=False)),
        # Reversed/Trim
        ([TEST_INPUT_FILE, '-mt', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=True, is_trim=True, verbosity=0)),
        ([TEST_INPUT_FILE, '-t', '--overwrite', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(overwrite=True,), move_files=False, is_trim=True)),
        ([TEST_INPUT_FILE, '-t', '--overwrite', '--exact', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(overwrite=True, exact=True), move_files=False, is_trim=True)),
        # Verbosity Level
        ([TEST_INPUT_FILE, '-v', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=1)),
        ([TEST_INPUT_FILE, '-vv', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=2)),
        ([TEST_INPUT_FILE, '-vvv', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_write(), move_files=False, verbosity=2)),
    ]
)
def test_validate_input_arguments_temp_dir_ts_input_str_1_with_data_dir_returns_data(
    test_input: list[str],
    expected: tuple[InputData, TemporaryDirectory],
):
    temp_dir = Path(expected[1].name)
    chdir(temp_dir)
    (input_file := (temp_dir / TEST_INPUT_FILE)).touch()
    input_file.write_text(TS_INPUT_STR_1)
    # Append the DataDir in the TempDir
    test_input.append(str(temp_dir / TEST_DATA_DIR))
    # Object Comparison
    assert expected[0] == validate_input_arguments(test_input)


@pytest.mark.parametrize(
    "test_input, expected", [
        # Note: Text Merge Increases Verbosity to minimum 1.
        ([TEST_INPUT_FILE, '--append', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=False), move_files=False)),
        ([TEST_INPUT_FILE, '--prepend', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=True), move_files=False)),
        # With MoveFiles
        ([TEST_INPUT_FILE, '--append', '-m', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=False), move_files=True)),
        ([TEST_INPUT_FILE, '--prepend', '-m', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=True), move_files=True)),
        # With Trim
        ([TEST_INPUT_FILE, '-t', '--append', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=False), move_files=False, is_trim=True)),
        ([TEST_INPUT_FILE, '-t', '--prepend', '--data_dir'], input_data_with_dir(TEST_INPUT_FILE, TEST_DATA_DIR, get_control_mode_text_merge(is_prepend=True), move_files=False, is_trim=True)),
    ]
)
def test_validate_input_arguments_temp_dir_ts_input_str_1_with_data_dir_text_merge_returns_data(
    test_input: list[str],
    expected: tuple[InputData, TemporaryDirectory],
):
    temp_dir = Path(expected[1].name)
    chdir(temp_dir)
    (input_file := (temp_dir / TEST_INPUT_FILE)).touch()
    input_file.write_text(TS_INPUT_STR_1)
    # Append the DataDir in the TempDir
    test_input.append(str(temp_dir / TEST_DATA_DIR))
    # Object Comparison
    assert expected[0] == validate_input_arguments(test_input)
