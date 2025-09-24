""" Testing Input Package Method: validate_input_arguments.
"""
from pathlib import Path
import os

import pytest

from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.input import validate_input_arguments, InputData, file_validation

from test.treescript_builder.input.conftest import MockPathStat


def test_validate_input_arguments_returns_input_data():
    tree_input_data = 'src/\n  data.txt'
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: tree_input_data)
        #
        result = validate_input_arguments(['tree_input'])
        assert result is not None
        assert result.data_dir is None
        assert not result.is_reversed
        assert result.tree_input == tree_input_data


def test_validate_input_arguments_input_file_does_not_exist_raises_error():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        with pytest.raises(SystemExit):
            validate_input_arguments(['tree_input'])


def test_validate_input_arguments_input_file_is_empty_returns_input_no_data_dir():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: '')
        result = validate_input_arguments(['tree_input'])
        assert result is not None
        assert result.data_dir is None


def test_validate_input_arguments_input_file_is_empty_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: '')
        with pytest.raises(SystemExit, match=file_validation._FILE_VALIDATION_ERROR_MSG):
            validate_input_arguments(['tree_input'])


def test_validate_input_arguments_unknown_argument_raises_error():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        with pytest.raises(SystemExit):
            validate_input_arguments(['tree_input', 'random-arg'])


TS_INPUT_STR_1 = 'src/\n  main_src_file.code'


def test_validate_input_arguments_sample_temp_dir(tmp_path: Path):
    (input_file := (tmp_path / 'tree_input')).touch()
    input_file.write_text(TS_INPUT_STR_1)
    os.chdir(tmp_path)
    #
    result: InputData = validate_input_arguments(['tree_input'])
    assert result.tree_input == TS_INPUT_STR_1
    assert result.data_dir is None
    assert not result.is_reversed
    assert result.mode == FileModeEnum.APPEND
    assert result.verbosity_level == 0


@pytest.mark.parametrize(
    "test_input, expected", [
        (['tree_input'], InputData(TS_INPUT_STR_1, mode=FileModeEnum.APPEND)),
        # Note: Cancel increases Verbosity to minimum 1
        (['tree_input', '-c'], InputData(TS_INPUT_STR_1, mode=FileModeEnum.CANCEL, verbosity_level=1)),
        (['tree_input', '-m'], InputData(TS_INPUT_STR_1, mode=FileModeEnum.MOVE)),
        (['tree_input', '-o'], InputData(TS_INPUT_STR_1, mode=FileModeEnum.OVERWRITE)),
        (['tree_input', '-p'], InputData(TS_INPUT_STR_1, mode=FileModeEnum.PREPEND)),
        # Reversed/Trim
        (['tree_input', '-cr'], InputData(TS_INPUT_STR_1, is_reversed=True, mode=FileModeEnum.CANCEL, verbosity_level=1)),
        (['tree_input', '-mr'], InputData(TS_INPUT_STR_1, is_reversed=True, mode=FileModeEnum.MOVE)),
        (['tree_input', '-or'], InputData(TS_INPUT_STR_1, is_reversed=True, mode=FileModeEnum.OVERWRITE)),
        (['tree_input', '-pr'], InputData(TS_INPUT_STR_1, is_reversed=True, mode=FileModeEnum.PREPEND)),
        # Verbosity Level
        (['tree_input', '-v'], InputData(TS_INPUT_STR_1, verbosity_level=1)),
        (['tree_input', '-vv'], InputData(TS_INPUT_STR_1, verbosity_level=2)),
        # When Combined with CANCEL:
        (['tree_input', '-cv'], InputData(TS_INPUT_STR_1, mode=FileModeEnum.CANCEL, verbosity_level=1)),
        (['tree_input', '-cvv'], InputData(TS_INPUT_STR_1, mode=FileModeEnum.CANCEL, verbosity_level=2)),
    ]
)
def test_validate_input_arguments_temp_dir_ts_input_str_1_returns_data(
    test_input: list[str],
    expected: InputData,
    tmp_path: Path,
):
    (input_file := (tmp_path / 'tree_input')).touch()
    input_file.write_text(TS_INPUT_STR_1)
    os.chdir(tmp_path)
    # Object Comparison
    assert expected == validate_input_arguments(test_input)


@pytest.mark.parametrize(
    "test_input, expected", [
        (['tree_input', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), mode=FileModeEnum.APPEND)),
        # Note: Cancel increases Verbosity to minimum 1.
        (['tree_input', '--data_dir', 'data', '-c'], InputData(TS_INPUT_STR_1, Path('data'), mode=FileModeEnum.CANCEL, verbosity_level=1)),
        (['tree_input', '--data_dir', 'data', '-m'], InputData(TS_INPUT_STR_1, Path('data'), mode=FileModeEnum.MOVE)),
        (['tree_input', '--data_dir', 'data', '-o'], InputData(TS_INPUT_STR_1, Path('data'), mode=FileModeEnum.OVERWRITE)),
        (['tree_input', '--data_dir', 'data', '-p'], InputData(TS_INPUT_STR_1, Path('data'), mode=FileModeEnum.PREPEND)),
        # Reversed/Trim
        (['tree_input', '-cr', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), is_reversed=True, mode=FileModeEnum.CANCEL, verbosity_level=1)),
        (['tree_input', '-mr', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), is_reversed=True, mode=FileModeEnum.MOVE)),
        (['tree_input', '-or', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), is_reversed=True, mode=FileModeEnum.OVERWRITE)),
        (['tree_input', '-pr', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), is_reversed=True, mode=FileModeEnum.PREPEND)),
        # Verbosity Level
        (['tree_input', '-v', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), verbosity_level=1)),
        (['tree_input', '-vv', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), verbosity_level=2)),
        (['tree_input', '-vvv', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), verbosity_level=2)),
        # Combined with CANCEL:
        (['tree_input', '-cv', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), mode=FileModeEnum.CANCEL, verbosity_level=1)),
        (['tree_input', '-cvv', '--data_dir', 'data'], InputData(TS_INPUT_STR_1, Path('data'), mode=FileModeEnum.CANCEL, verbosity_level=2)),
    ]
)
def test_validate_input_arguments_temp_dir_ts_input_str_1_with_data_dir_returns_data(
    test_input: list[str],
    expected: InputData,
    tmp_path: Path,
):
    (input_file := (tmp_path / 'tree_input')).touch()
    input_file.write_text(TS_INPUT_STR_1)
    (tmp_path / 'data').mkdir()
    os.chdir(tmp_path)
    # Object Comparison
    assert expected == validate_input_arguments(test_input)
