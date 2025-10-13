""" Testing Argument Parsing Module.
"""
import pytest

from test.conftest import TEST_DATA_DIR
from treescript_builder.input.argument_parser import parse_arguments, _INVALID_ARGUMENTS_COMBINATION_STR, \
    _INVALID_CONTROL_MODE_ARGUMENTS_STR, _INVALID_TEXT_MODE_ARGUMENTS_STR
from treescript_builder.input.argument_data import ArgumentData


_TS_FILE_NAME = "tree_file"


def test_parse_arguments_none_raises_typeerror():
    with pytest.raises(TypeError):
        parse_arguments(None)


def test_parse_arguments_int_raises_typeerror():
    with pytest.raises(TypeError):
        parse_arguments(2)


def test_parse_arguments_empty_list_raises_exit():
    with pytest.raises(SystemExit, match='The TreeScript file path argument is required.'):
        parse_arguments([])


@pytest.mark.parametrize(
    "test_input",
    [
        ([""]),                             # Empty Str
        ([" "]),                            # Single space char
        (["--data"]),                       # missing positional argument
        (["-f"]),                           # This is not a valid flag + Missing positional argument
        ([_TS_FILE_NAME, "--data_dir="]),   # missing DataDir argument
    ]
)
def test_parse_arguments_raises_system_exit(test_input):
    with pytest.raises(SystemExit):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    'test_input, expected_text_append, expected_text_prepend', [
        ([_TS_FILE_NAME], False, False),                # Default Text Mode
        ([_TS_FILE_NAME, '--append'], True, False),     # Append Text Mode
        ([_TS_FILE_NAME, '--prepend'], False, True),    # Prepend Text Mode
        # Shortcut arguments.
        ([_TS_FILE_NAME, '--app'], True, False),        # Append Text Mode Short
        ([_TS_FILE_NAME, '--pre'], False, True),        # Prepend Text Mode Short
    ]
)
def test_parse_arguments_defaults_parametrized_text_modes_valid(
    test_input, expected_text_append, expected_text_prepend
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str=None,
        text_append=expected_text_append,
        text_prepend=expected_text_prepend,
    )


@pytest.mark.parametrize(
    "test_input, expect_prepend_mode, expect_trim, expect_move", [
        # Prepend TextMode
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--prepend'], True, False, False),
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--prepend', '--move'], True, False, True),
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--prepend', '-m'], True, False, True),
        # Append TextMode
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--append'], False, False, False),
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--append', '--move'], False, False, True),
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--append', '-m'], False, False, True),
        # Prepend w/ Trim
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '-t', '--prepend'], True, True, False),
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '-mt', '--prepend'], True, True, True),
        # Append w/ Trim
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '-t', '--append'], False, True, False),
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '-mt', '--append'], False, True, True),
    ]
)
def test_parse_arguments_data_dir_parametrized_text_modes_valid(
    test_input, expect_prepend_mode, expect_trim, expect_move,
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str=TEST_DATA_DIR,
        trim_tree=expect_trim,
        move_files=expect_move,
        text_append=expect_prepend_mode == False,   # Must be either Append or Prepend!
        text_prepend=expect_prepend_mode,
    )


@pytest.mark.parametrize(
    'test_input, expect_continue, expect_validate, expect_overwrite, expect_exact', [
        ([_TS_FILE_NAME], False, False, False, False),                           # Default Text Mode
        ([_TS_FILE_NAME, '--continue'], True, False, False, False),              # Continue Control Mode
        ([_TS_FILE_NAME, '--validate'], False, True, False, False),              # Validate Control Mode
        ([_TS_FILE_NAME, '--overwrite'], False, False, True, False),             # Overwrite Control Mode
        ([_TS_FILE_NAME, '--overwrite', '--exact'], False, False, True, True),   # Overwrite Exact Control Mode
        # Shortcut arguments.
        ([_TS_FILE_NAME, '--con'], True, False, False, False),                   # Continue Control Mode
        ([_TS_FILE_NAME, '--val'], False, True, False, False),                   # Validate Control Mode
        ([_TS_FILE_NAME, '--over'], False, False, True, False),                  # Overwrite Control Mode
        ([_TS_FILE_NAME, '--over', '--ex'], False, False, True, True),           # Overwrite Control Mode
    ]
)
def test_parse_arguments_defaults_parametrized_control_modes_valid(
    test_input, expect_continue, expect_validate, expect_overwrite, expect_exact
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str=None,
        control_continue=expect_continue,
        control_validate=expect_validate,
        control_overwrite=expect_overwrite,
        control_exact_build=expect_exact,
    )


@pytest.mark.parametrize(
    'test_input, expected_trim, expected_move', [
        ([_TS_FILE_NAME], False, False),                    # Default
        ([_TS_FILE_NAME, '--trim'], True, False),           # Trim Tree
        ([_TS_FILE_NAME, '--move'], False, True),           # Move Files
        ([_TS_FILE_NAME, '--move', '--trim'], True, True),  # Move and Trim 
        # Shortcut arguments.
        ([_TS_FILE_NAME, '-t'], True, False),               # Trim Tree Short
        ([_TS_FILE_NAME, '-m'], False, True),               # Move Files Short
        ([_TS_FILE_NAME, '-mt'], True, True),               # Move and Trim Short
    ]
)
def test_parse_arguments_defaults_parametrized_modifiers_valid(
    test_input, expected_trim, expected_move
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str=None,
        trim_tree=expected_trim,
        move_files=expected_move,
    )


@pytest.mark.parametrize(
    'test_input, expected_trim, expected_move', [
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}"], False, False),                     # Default
        ([_TS_FILE_NAME, "--data_dir", TEST_DATA_DIR], False, False),                  # Default 2
        #
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--trim'], True, False),            # Trim Tree
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '-t'], True, False),                # Trim Tree Short
        #
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--move'], False, True),            # Move Files
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '-m'], False, True),                # Move Files Short
        #
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '--move', '--trim'], True, True),   # Move and Trim 
        ([_TS_FILE_NAME, f"--data_dir={TEST_DATA_DIR}", '-mt'], True, True),                # Move and Trim Short
    ]
)
def test_parse_arguments_data_dir_parametrized_modifiers_valid(
    test_input, expected_trim, expected_move
):
    assert parse_arguments(test_input) == ArgumentData(
        input_file_path_str=_TS_FILE_NAME,
        data_dir_path_str=TEST_DATA_DIR,
        trim_tree=expected_trim,
        move_files=expected_move,
    )


@pytest.mark.parametrize(
    "test_input, expected_verbosity", [
        ([_TS_FILE_NAME, "-v"], 1), # <- Verbose is an Argument that Counts.
        ([_TS_FILE_NAME, "-vv"], 2),
        ([_TS_FILE_NAME, "-vvv"], 2), # <- Additional (beyond max 2) are ignored in validation logic.
        ([_TS_FILE_NAME, "--verbosity"], 1),
        ([_TS_FILE_NAME, "--verbos",], 1), # <- Partial Argument.
        ([_TS_FILE_NAME, "--verbosity", "--verbosity"], 2), # <- Technically valid.
    ]
)
def test_parse_arguments_defaults_parametrized_verbosity_valid(
    test_input, expected_verbosity
):
    assert expected_verbosity == parse_arguments(test_input).verbosity


@pytest.mark.parametrize(
    "test_input", [
        ([_TS_FILE_NAME, '--append', "--prepend"]),
    ]
)
def test_parse_arguments_invalid_text_mode_combinations_raises_exit(test_input):
    from re import escape
    with pytest.raises(SystemExit, match=escape(_INVALID_TEXT_MODE_ARGUMENTS_STR)):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input", [
        ([_TS_FILE_NAME, '--continue', "--exact"]), # Exact without overwrite? Should exact imply overwrite?
        ([_TS_FILE_NAME, "--validate", "--exact", '-t']), # W/ Trim and Validate arguments
    ]
)
def test_parse_arguments_invalid_control_mode_combinations_raises_exit(test_input):
    from re import escape
    with pytest.raises(SystemExit, match=escape(_INVALID_CONTROL_MODE_ARGUMENTS_STR)):
        parse_arguments(test_input)


@pytest.mark.parametrize(
    "test_input", [
        # The Cancel Argument is not included, because it is default. Continue argument.
        ([_TS_FILE_NAME, '--continue', "--cancel"]), # Continue and Cancel are different behaviours.
        ([_TS_FILE_NAME, "--cancel", "--overwrite"]),
    ]
)
def test_parse_arguments_invalid_control_mode_combinations2_raises_exit(test_input):
    with pytest.raises(SystemExit):
        parse_arguments(test_input)
