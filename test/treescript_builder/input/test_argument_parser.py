""" Testing Argument Parsing Module.
"""
import pytest

from treescript_builder.input import parse_arguments
from treescript_builder.input.argument_data import ArgumentData


@pytest.mark.parametrize(
    "test_input",
    [
        ([]),
        ([""]),
        ([" "]),
        (["--data"]),
        (["-f"]),
        (["tree_file", "--data_dir="]),
    ]
)
def test_parse_arguments_raises_value_error(test_input):
    with pytest.raises(SystemExit):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input,expect",
    [
        (["tree_file"], ArgumentData("tree_file", None, False)),
        (["tree_file"], ArgumentData("tree_file", None, False)),
        (["tree_file", "--data_dir=data"], ArgumentData("tree_file", "data", False)),
        (["tree_file", "--data_dir=data", "-r"], ArgumentData("tree_file", "data", True)),
        (["tree_file", "--data_dir=data", "-r"], ArgumentData("tree_file", "data", True)),
        (["tree_file", "-r"], ArgumentData("tree_file", None, True)),
        (["tree_file", "--reverse"], ArgumentData("tree_file", None, True)),
        (["tree_file", "--trim"], ArgumentData("tree_file", None, True)),
    ]
)
def test_parse_arguments_returns_data(test_input, expect):
    assert parse_arguments(test_input) == expect