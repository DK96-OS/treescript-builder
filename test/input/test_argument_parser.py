"""Testing Argument Parsing Module.
"""
import pytest
from input.argument_data import ArgumentData
from input.argument_parser import parse_arguments


@pytest.mark.xfail(raises=SystemExit, reason="invalid arguments")
@pytest.mark.parametrize(
    "test_input",
    [
        ([]),
        ([""]),
        ([" "]),
        (["--data"]),
        (["-f"]),
        (["tree_file", "--data_dir="]),
        (["tree_file", "-r"]),
        (["tree_file", "--reverse"]),
    ]
)
def test_parse_arguments_raises_value_error(test_input):
    with pytest.raises(SystemExit) as exit_info:
        parse_arguments(test_input)
    assert exit_info.type == SystemExit


@pytest.mark.parametrize(
    "test_input,expect",
    [
        (["tree_file"], ArgumentData("tree_file", None, False)),
        (["tree_file"], ArgumentData("tree_file", None, False)),
        (["tree_file", "--data_dir=data"], ArgumentData("tree_file", "data", False)),
        (["tree_file", "--data_dir=data", "-r"], ArgumentData("tree_file", "data", True)),
        (["tree_file", "--data_dir=data", "-r"], ArgumentData("tree_file", "data", True)),
    ]
)
def test_parse_arguments_returns_data(test_input, expect):
    assert parse_arguments(test_input) == expect
