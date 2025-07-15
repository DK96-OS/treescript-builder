""" Testing Init Module
"""
from pathlib import Path
import pytest

from test.treescript_builder.conftest import create_depth
from treescript_builder.input import validate_input_arguments


@pytest.mark.parametrize(
    "test_input,expect",
    [
        (0, 0),
        (1, 2),
        (2, 4),
        (4, 8),
    ]
)
def test_create_depth_returns_expected(test_input, expect):
    assert len(create_depth(test_input)) == expect


def test_create_depth_negative_numbers_returns_empty():
    assert '' == create_depth(-1)


def test_validate_input_arguments_returns_input_data():
    tree_input_data = 'src/\n  data.txt'
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
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
        with pytest.raises(SystemExit):
            validate_input_arguments(['tree_input'])


def test_validate_input_arguments_input_file_is_empty_returns_input_no_data_dir():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: '')
        result = validate_input_arguments(['tree_input'])
        assert result is not None
        assert result.data_dir is None


def test_validate_input_arguments_unknown_argument_raises_error():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        with pytest.raises(SystemExit):
            validate_input_arguments(['tree_input', 'random-arg'])
