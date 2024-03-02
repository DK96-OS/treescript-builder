"""Testing Argument Parsing Module.
"""
import pytest
from input.argument_parsing import parse_arguments


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
    try:
        parse_arguments(test_input)
    except ValueError as E:
        assert True
    finally:
        assert False


@pytest.mark.parametrize(
    "test_input,expect",
    [
        (["tree_file"], ArgumentData("tree_file", None, False)),
        (["tree_file", "-r"], ArgumentData("tree_file", None, True),
        (["tree_file", "--reversed"], ArgumentData("tree_file", None, True),
        (["tree_file"], ArgumentData("tree_file", None, False)),
        (["tree_file", "--data_dir=data"], ArgumentData("tree_file", "data", False)),
        (["tree_file", "--data_dir=data", "-r"], ArgumentData("tree_file", "data", True)),
        (["tree_file", "--data_dir=data", "-r"], ArgumentData("tree_file", "data", True)),
    ]
)
def test_parse_arguments_raises_value_error(test_input, expect):
    assert parse_arguments(test_input) == expect
