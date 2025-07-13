""" Testing Argument Parsing Module.
"""
import pytest

from treescript_builder.input import parse_arguments
from treescript_builder.input.argument_data import ArgumentData


def test_parse_arguments_empty_list_raises_exit():
    with pytest.raises(SystemExit, match='The TreeScript file path argument is required.'):
        parse_arguments([])
        

def test_parse_arguments_none_raises_exit():
    with pytest.raises(SystemExit, match='The TreeScript file path argument is required.'):
        parse_arguments(None)


@pytest.mark.parametrize(
    "test_input",
    [
        ([""]),
        ([" "]),
        (["--data"]),
        (["-f"]),
        (["tree_file", "--data_dir="]),
    ]
)
def test_parse_arguments_raises_system_exit(test_input):
    with pytest.raises(SystemExit):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input,expect",
    [
        # No DataDir, Just Shorthand Options
        (["tree_file"], ArgumentData("tree_file", None, False, False, False)),
        (["tree_file", "-p"], ArgumentData("tree_file", None, False, False, True)),
        (["tree_file", "-o"], ArgumentData("tree_file", None, False, True, False)),
        (["tree_file", "-r"], ArgumentData("tree_file", None, True, False, False)),
        (["tree_file", "-pr"], ArgumentData("tree_file", None, True, False, True)),
        (["tree_file", "-or"], ArgumentData("tree_file", None, True, True, False)),
        # Data Dir, And Shorthand Options
        (["tree_file", "--data_dir=data"], ArgumentData("tree_file", "data", False, False, False)),
        (["tree_file", "--data_dir=data", "-p"], ArgumentData("tree_file", "data", False, False, True)),
        (["tree_file", "--data_dir=data", "-o"], ArgumentData("tree_file", "data", False, True, False)),
        (["tree_file", "--data_dir=data", "-r"], ArgumentData("tree_file", "data", True, False, False)),
        (["tree_file", "--data_dir=data", "-ro"], ArgumentData("tree_file", "data", True, True, False)),
        (["tree_file", "--data_dir", "data", "-rp"], ArgumentData("tree_file", "data", True, False, True)),
        # Full Arg Names
        (["tree_file", "--reverse"], ArgumentData("tree_file", None, True, False, False)),
        (["tree_file", "--trim"], ArgumentData("tree_file", None, True, False, False)),
        (["tree_file", "--overwrite"], ArgumentData("tree_file", None, False, True, False)),
        (["tree_file", "--prepend"], ArgumentData("tree_file", None, False, False, True)),
        (["tree_file", "--overwrite", '--reverse'], ArgumentData("tree_file", None, True, True, False)),
        (["tree_file", "--prepend", '--reverse'], ArgumentData("tree_file", None, True, False, True)),
    ]
)
def test_parse_arguments_returns_data(test_input, expect):
    assert parse_arguments(test_input) == expect


@pytest.mark.parametrize(
    "test_input", [
        (["tree_file", "-po"]),
        (["tree_file", "-rpo"]),
        (["tree_file", '--reverse', "-po"]),
        (["tree_file", '--reverse', "-po", "--data_dir", "data"]),
    ]
)
def test_parse_arguments_invalid_option_combinations_raise_system_exit(test_input):
    with pytest.raises(SystemExit, match='Invalid Option Combination.'):
        parse_arguments(test_input)
