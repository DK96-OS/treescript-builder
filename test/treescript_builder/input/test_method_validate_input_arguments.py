""" Testing Input Package Method: validate_input_arguments.
"""
from pathlib import Path

import pytest

from test.treescript_builder.input.conftest import MockPathStat
from treescript_builder.input import validate_input_arguments, file_validation


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
