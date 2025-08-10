""" Defines and Validates Argument Syntax.
 - Encapsulates Argument Parser.
 - Returns Argument Data, the args provided by the User.
 Author: DK96-OS 2024 - 2025
"""
from argparse import ArgumentParser
from sys import exit

from treescript_builder.input.argument_data import ArgumentData
from treescript_builder.input.string_validation import validate_name


def parse_arguments(
    args: list[str],
) -> ArgumentData:
    """ Parse command line arguments.

**Parameters:**
 - args(list): A list of argument strings.

**Returns:**
 ArgumentData - Container for Valid Argument Data.
    """
    if args is None or not isinstance(args, list):
        raise TypeError
    elif len(args) == 0:
        exit(_REQUIRED_ARGUMENT_NOT_FOUND_STR)
    try: # Initialize the Parser and Parse Immediately
        parsed_args = _define_arguments().parse_args(args)
    except SystemExit:
        exit("Unable to Parse Arguments.")
    return _validate_arguments(
        parsed_args.tree_file_name,
        parsed_args.data_dir,
        parsed_args.reverse,
        parsed_args.overwrite,
        parsed_args.prepend,
        parsed_args.cancel,
        parsed_args.move,
        parsed_args.verbosity
    )


_CLI_DESCRIPTION_STR: str = "TreeScript-Builder: The FileTree Builder and Trimmer."

_REQUIRED_ARGUMENT_NOT_FOUND_STR: str = "The TreeScript file path argument is required."
_INVALID_TREESCRIPT_FILE_STR: str = "TreeScript file argument was invalid."
_INVALID_ARGUMENTS_COMBINATION_STR: str = "Invalid Option Combination.\n\nProvide only one of these options:\n--cancel, --move, --overwrite, --prepend.\n(Default: Append)"


def _validate_arguments(
    tree_file_name: str | None,
    data_dir_name: str | None,
    is_reverse: bool | None,
    overwrite: bool | None,
    prepend: bool | None,
    cancel: bool | None,
    move: bool | None,
    verbosity: int | None,
) -> ArgumentData:
    """ Checks the values received from the ArgParser.
 - Uses Validate Name method from StringValidation.
 - Ensures that Reverse Operations have a Data Directory.
 - Includes NoneType state for all Parameters to improve TypeChecking.
 - This is a reminder to keep the union types, and always validate Namespace object attributes.

**Parameters:**
 - tree_file_name (str): The file name of the tree input.
 - data_dir_name (str?): The Data Directory name.
 - is_reverse (bool?): Whether the builder operation is reversed.
 - overwrite (bool?): Option to Overwrite the data in existing files.
 - prepend (bool?): Option to Prepend the data, to the start of each file.
 - cancel (bool?): Optional FileMode that cancels any operation that may overwrite existing file contents.
 - move (bool?): Optional FileMode that moves files instead of copying.
 - verbosity (int?): The level of output to print. Min 0, Max 2.

**Returns:**
 ArgumentData - A DataClass of syntactically correct arguments.
    """
    # Validate Required Positional TreeName Argument
    if not validate_name(tree_file_name):
        exit(_INVALID_TREESCRIPT_FILE_STR)
    # Typecheck Boolean Flags and Verbosity Counter, if the values are present.
    if is_reverse is not None and not isinstance(is_reverse, bool) or\
            overwrite is not None and not isinstance(overwrite, bool) or\
            prepend is not None and not isinstance(prepend, bool) or\
            cancel is not None and not isinstance(cancel, bool) or\
            move is not None and not isinstance(move, bool) or\
            verbosity is not None and not isinstance(verbosity, int):
        raise TypeError
    # Validate The Option Combination
    mutually_exclusive_options: tuple[bool, ...] = (overwrite, prepend, cancel, move)
    if (option_sum := sum(1 if X else 0 for X in mutually_exclusive_options)) > 1:
        exit(_INVALID_ARGUMENTS_COMBINATION_STR) # Maximum of 1 option in this group
    elif option_sum == 0:
        pass # Default FileMode: Append
    # Validate Verbosity level
    if (verbosity := min(verbosity, 2)) < 0:
        raise ValueError
    # Validate DataDirectory Name if Present
    if data_dir_name is not None and not validate_name(data_dir_name):
        exit("The Data Directory argument was invalid.")
    # Ready.
    return ArgumentData(
        input_file_path_str=tree_file_name,
        data_dir_path_str=data_dir_name,
        is_reversed=is_reverse,
        overwrite=overwrite,
        prepend=prepend,
        cancel=cancel,
        move=move,
        verbosity=verbosity,
    )


def _define_arguments() -> ArgumentParser:
    """ Initializes and Defines Argument Parser.
 - Sets Required/Optional Arguments and Flags.

**Returns:**
 argparse.ArgumentParser - An instance with all supported FTB Arguments.
    """
    parser = ArgumentParser(
        description=_CLI_DESCRIPTION_STR,
    )
    # Required argument
    parser.add_argument(
        'tree_file_name',
        type=str,
        help='The File containing the Tree Node Structure'
    )
    # Optional arguments
    parser.add_argument(
        '--data_dir',
        default=None,
        help='The Data Directory'
    )
    parser.add_argument(
        '-r',
        '--reverse',
        '--trim', # There is no '-t' shortcut! The '-r' is enough.
        action='store_true',
        default=False,
        help='The Trim operation is the reverse of the FileTree Build operation. Only -r shortcut is provided.'
    )
    parser.add_argument(
        '-o',
        '--overwrite',
        action='store_true',
        default=False,
        help='Flag to overwrite files with data.'
    )
    parser.add_argument(
        '-p',
        '--prepend',
        action='store_true',
        default=False,
        help='Flag to insert data at the start of files.'
    )
    parser.add_argument(
        '-c',
        '--cancel',
        action='store_true',
        default=False,
        help='Flag to cancel any file operation where the target file already contains data.'
    )
    parser.add_argument(
        '-m',
        '--move',
        action='store_true',
        default=False,
        help='Flag to move all files instead of copying.'
    )
    parser.add_argument(
        '-v',
        '--verbosity',
        action='count',
        default=0,
        help='Verbose Levels of CLI output.\n - L0: No Output.\n - L1: Failed FileTree Operations.\n - L2: All FileTree Operations.'
    )
    return parser
