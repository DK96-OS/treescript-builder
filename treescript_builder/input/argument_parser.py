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
        tree_file_name=parsed_args.tree_file_name,
        data_dir_name=parsed_args.data_dir,
        is_reverse=parsed_args.trim,
        move=parsed_args.move_files,
        text_append=parsed_args.append,
        text_prepend=parsed_args.prepend,
        control_validate=parsed_args.validate,
        control_overwrite=parsed_args.overwrite,
        control_exact_build=parsed_args.exact,
        control_continue=parsed_args.__dict__['continue'],
        verbosity=parsed_args.verbosity,
    )


_CLI_DESCRIPTION_STR: str = "TreeScript-Builder: The FileTree Builder and Trimmer."

_REQUIRED_ARGUMENT_NOT_FOUND_STR: str = "The TreeScript file path argument is required."
_INVALID_TREESCRIPT_FILE_STR: str = "TreeScript file argument was invalid."
_INVALID_ARGUMENTS_COMBINATION_STR: str = "Invalid Option Combination.\n\nProvide only one of these options:\n--cancel, --move, --overwrite, --prepend.\n(Default: Append)"

_INVALID_TEXT_MODE_ARGUMENTS_STR: str = 'Invalid TextMode argument(s).'
_INVALID_CONTROL_MODE_ARGUMENTS_STR: str = 'Invalid Control argument(s).'
_INVALID_DATA_DIR_ARGUMENT_STR: str = 'Invalid DataDirectory argument.'


def _validate_arguments(
    tree_file_name: str | None,
    data_dir_name: str | None,
    is_reverse: bool | None,
    move: bool | None,
    text_append: bool | None,
    text_prepend: bool | None,
    control_validate: bool | None,
    control_overwrite: bool | None,
    control_exact_build: bool | None,
    control_continue: bool | None,
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
            move is not None and not isinstance(move, bool) or\
            text_append is not None and not isinstance(text_append, bool) or\
            text_prepend is not None and not isinstance(text_prepend, bool) or\
            control_validate is not None and not isinstance(control_validate, bool) or\
            control_overwrite is not None and not isinstance(control_overwrite, bool) or\
            control_exact_build is not None and not isinstance(control_exact_build, bool) or\
            control_continue is not None and not isinstance(control_continue, bool) or\
            verbosity is not None and not isinstance(verbosity, int):
        raise TypeError
    # Validate TextMode: Maximum of 1.
    if text_prepend and text_append:
        # Cannot do both Append and Prepend in one operation.
        raise exit(_INVALID_TEXT_MODE_ARGUMENTS_STR)
    # Validate ControlMode Arguments
    if control_exact_build:
        # Ensure Overwrite is present if exact_build is used.
        if control_overwrite or text_append or text_prepend:
            pass # Overwrite is present in args, or implied.
        else: # exact_build without overwrite is an invalid combination.
            raise exit(_INVALID_CONTROL_MODE_ARGUMENTS_STR)
    # Validate Verbosity level
    if (verbosity := min(verbosity, 2)) < 0:
        raise ValueError
    # Validate DataDirectory Name if Present
    if data_dir_name is not None and not validate_name(data_dir_name):
        exit(_INVALID_DATA_DIR_ARGUMENT_STR)
    # Ready.
    return ArgumentData(
        input_file_path_str=tree_file_name,
        data_dir_path_str=data_dir_name,
        trim_tree=is_reverse,
        move_files=move,
        text_append=text_append,
        text_prepend=text_prepend,
        control_validate=control_validate,
        control_overwrite=control_overwrite,
        control_exact_build=control_exact_build,
        control_continue=control_continue,
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
        help='The File containing TreeScript.'
    )
    # Optional arguments
    parser.add_argument(
        '--data_dir',
        default=None,
        help='The Data Directory'
    )
    parser.add_argument(
        '-t',
        '--trim',
        action='store_true',
        default=False,
        help='The Trim operation is the inverse of the FileTree Build operation.'
    )
    parser.add_argument(
        '-m',
        '--move_files',
        action='store_true',
        default=False,
        help='Flag to move files instead of copying.'
    )
    parser.add_argument(
        '--append',
        action='store_true',
        default=False,
        help='Flag to insert text data at the end of files.'
    )
    parser.add_argument(
        '--prepend',
        action='store_true',
        default=False,
        help='Flag to insert text data at the start of files.'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        default=False,
        help='ControlMode option that increases the scope of the validation phase, then runs the build in Cancel ControlMode. Raises Minimum Verbosity to 1.'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        default=False,
        help='ControlMode option to enable overwriting Target files if they already exist. Raises Minimum Verbosity to 1.'
    )
    parser.add_argument(
        '--exact',
        action='store_true',
        default=False,
        help='ControlMode option to override build safety feature, allowing overwriting Target files even if Data is empty.'
    )
    parser.add_argument(
        '--continue',
        action='store_true',
        default=False,
        help='ControlMode option to continue the build if an error occurs. Raises Minimum Verbosity to 1.'
    )
    parser.add_argument(
        '-v',
        '--verbosity',
        action='count',
        default=0,
        help='Levels of Verbosity in Command Line output. Note: Exits and Exceptions are unaffected by this argument.\n - L0: No Output.\n - L1: Failed FileTree Operations.\n - L2: All FileTree Operations.'
    )
    return parser
