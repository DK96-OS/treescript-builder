""" Testing Argument Parsing Module.
"""
import pytest

from treescript_builder.input import parse_arguments, argument_parser
from treescript_builder.input.argument_data import ArgumentData


_TS_FILE_NAME = "tree_file"


def test_parse_arguments_empty_list_raises_exit():
    with pytest.raises(SystemExit, match='The TreeScript file path argument is required.'):
        parse_arguments([])


def test_parse_arguments_none_raises_typeerror():
    with pytest.raises(TypeError):
        parse_arguments(None)


def test_parse_arguments_int_raises_typeerror():
    with pytest.raises(TypeError):
        parse_arguments(2)


@pytest.mark.parametrize(
    "test_input",
    [
        ([""]),
        ([" "]),
        (["--data"]),
        (["-f"]),
        ([_TS_FILE_NAME, "--data_dir="]),
    ]
)
def test_parse_arguments_raises_system_exit(test_input):
    with pytest.raises(SystemExit):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend",
    [
        # No DataDir, Just Shorthand Options
        ([_TS_FILE_NAME], False, False, False, False),
        ([_TS_FILE_NAME, "-c"], True, False, False, False),
        ([_TS_FILE_NAME, "-m"], False, True, False, False),
        ([_TS_FILE_NAME, "-o"], False, False, True, False),
        ([_TS_FILE_NAME, "-p"], False, False, False, True),
    ]
)
def test_parse_arguments_returns_data(test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str=None,
        is_reversed=False,
        verbosity=0,
        cancel=bool_cancel,
        move=bool_move,
        prepend=bool_prepend,
        overwrite=bool_overwrite,
    )


@pytest.mark.parametrize(
    "test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend",
    [
        ([_TS_FILE_NAME, "-r"], False, False, False, False),
        ([_TS_FILE_NAME, "-cr"], True, False, False, False),
        ([_TS_FILE_NAME, "-mr"], False, True, False, False),
        ([_TS_FILE_NAME, "-or"], False, False, True, False),
        ([_TS_FILE_NAME, "-pr"], False, False, False, True),
    ]
)
def test_parse_arguments_reverse_shorthand_options_returns_data(
    test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str=None,
        is_reversed=True,
        verbosity=0,
        cancel=bool_cancel,
        move=bool_move,
        prepend=bool_prepend,
        overwrite=bool_overwrite,
    )


@pytest.mark.parametrize(
    "test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend",
    [
        # Data Dir, And Shorthand Options
        ([_TS_FILE_NAME, "--data_dir=data"], False, False, False, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-c"], True, False, False, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-m"], False, True, False, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-o"], False, False, True, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-p"], False, False, False, True),
    ]
)
def test_parse_arguments_datadir_returns_data(
    test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str='data',
        is_reversed=False,
        verbosity=0,
        cancel=bool_cancel,
        move=bool_move,
        prepend=bool_prepend,
        overwrite=bool_overwrite,
    )


@pytest.mark.parametrize(
    "test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend",
    [
        # DataDir Reversed, And Shorthand Options
        ([_TS_FILE_NAME, "--data_dir=data", "-r"], False, False, False, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-rc"], True, False, False, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-rm"], False, True, False, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-ro"], False, False, True, False),
        ([_TS_FILE_NAME, "--data_dir=data", "-rp"], False, False, False, True),
        # Also, with split datadir args:
        ([_TS_FILE_NAME, "--data_dir", "data", "-r"], False, False, False, False),
        ([_TS_FILE_NAME, "--data_dir", "data", "-rc"], True, False, False, False),
        ([_TS_FILE_NAME, "--data_dir", "data", "-rm"], False, True, False, False),
        ([_TS_FILE_NAME, "--data_dir", "data", "-ro"], False, False, True, False),
        ([_TS_FILE_NAME, "--data_dir", "data", "-rp"], False, False, False, True),
    ]
)
def test_parse_arguments_datadir_reversed_returns_data(
    test_input, bool_cancel, bool_move, bool_overwrite, bool_prepend
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str='data',
        is_reversed=True,
        verbosity=0,
        cancel=bool_cancel,
        move=bool_move,
        prepend=bool_prepend,
        overwrite=bool_overwrite,
    )


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ([_TS_FILE_NAME, "--reverse"], ArgumentData(_TS_FILE_NAME, None, True, 0, False, False, False, False)),
        ([_TS_FILE_NAME, "--trim"], ArgumentData(_TS_FILE_NAME, None, True, 0, False, False, False, False)),
        ([_TS_FILE_NAME, "--overwrite"], ArgumentData(_TS_FILE_NAME, None, False, 0, False, False, True, False)),
        ([_TS_FILE_NAME, "--prepend"], ArgumentData(_TS_FILE_NAME, None, False, 0, False, False, False, True)),
        ([_TS_FILE_NAME, "--overwrite", '--reverse'], ArgumentData(_TS_FILE_NAME, None, True, 0, False, False, True, False)),
        ([_TS_FILE_NAME, "--prepend", '--reverse'], ArgumentData(_TS_FILE_NAME, None, True, 0, False, False, False, True)),
        ([_TS_FILE_NAME, "--verbosity", '--reverse'], ArgumentData(_TS_FILE_NAME, None, True, 1, False, False, False, False)),
    ]
)
def test_parse_arguments_full_argument_names_returns_data(test_input, expect):
    assert parse_arguments(test_input) == expect


@pytest.mark.parametrize(
    "test_input", [
        ([_TS_FILE_NAME, "-rpo"]),
        ([_TS_FILE_NAME, '--reverse', "-po"]),
        ([_TS_FILE_NAME, '--reverse', "-po", "--data_dir", "data"]),
    ]
)
def test_parse_arguments_invalid_option_combinations_raises_exit(test_input):
    with pytest.raises(SystemExit, match='Invalid Option Combination.'):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input", [
        ([_TS_FILE_NAME, "-op"]),
        ([_TS_FILE_NAME, "-po"]), # <- Reverse order should not matter
        ([_TS_FILE_NAME, "-co"]), # The rest are unique combinations, sorted alphabetically.
        ([_TS_FILE_NAME, "-mo"]),
        ([_TS_FILE_NAME, "-cp"]),
        ([_TS_FILE_NAME, "-mp"]),
        ([_TS_FILE_NAME, "-cm"]),
    ]
)
def test_parse_arguments_invalid_file_mode_option_combinations_raises_exit(test_input):
    from re import escape
    with pytest.raises(SystemExit, match=escape(argument_parser._INVALID_ARGUMENTS_COMBINATION_STR)):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input", [
        ([_TS_FILE_NAME, "-por"]),
        ([_TS_FILE_NAME, "-cmr"]),
        ([_TS_FILE_NAME, "-cmopr"]),
        ([_TS_FILE_NAME, '--reverse', "-po"]),
        ([_TS_FILE_NAME, '--reverse', "-cm"]),
        ([_TS_FILE_NAME, '--trim', "-cm"]),
        ([_TS_FILE_NAME, '--reverse', "-po", "--data_dir", "data"]),
        ([_TS_FILE_NAME, '--reverse', "-cm", "--data_dir", "data"]),
    ]
)
def test_parse_arguments_reverse_with_invalid_option_combinations_with_more_args_raises_exit(test_input):
    with pytest.raises(SystemExit, match='Invalid Option Combination.'):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input, expected", [
        ([_TS_FILE_NAME, "-v"], 1), # <- Verbose is an Argument that Counts.
        ([_TS_FILE_NAME, "-vv"], 2),
        ([_TS_FILE_NAME, "-vvv"], 2), # <- Additional (beyond max 2) are ignored in validation logic.
        ([_TS_FILE_NAME, "--verbosity"], 1),
        ([_TS_FILE_NAME, "--verbos",], 1), # <- Partial Argument.
        ([_TS_FILE_NAME, "--verbosity", "--verbosity"], 2), # <- Technically valid.
    ]
)
def test_parse_arguments_verbosity_returns_argument_data(test_input, expected):
    assert expected == parse_arguments(test_input).verbosity
