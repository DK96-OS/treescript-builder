"""Testing Init Module"""
from pathlib import Path
import pytest

from input import validate_input_arguments


def test_validate_input_arguments_returns_input_data():
    tree_input_data = 'src/\n  data.txt'
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: tree_input_data)
        #
        result = validate_input_arguments(['tree_input'])
        assert result is not None
        assert result.data_dir is None
        assert result.is_reversed == False
        assert result.tree_input == tree_input_data


def test_validate_input_arguments_input_file_does_not_exist_raises_error():
    tree_input_data = 'src/\n  data.txt'
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        #
        try:
            validate_input_arguments(['tree_input'])
            assert False
        except SystemExit as e:
            assert True


def test_validate_input_arguments_input_file_is_empty_raises_error():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: '')
        try:
            validate_input_arguments(['tree_input'])
            assert False
        except SystemExit as e:
            assert True


def test_validate_input_arguments_unknown_argument_raises_error():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        try:
            validate_input_arguments(['tree_input', 'random-arg'])
            assert False
        except SystemExit as e:
            assert True
