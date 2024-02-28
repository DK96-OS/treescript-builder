"""Defines and Validates Argument Syntax.
"""
from argparse import ArgumentParser
from input.argument_data import ArgumentData
from typing import Optional


def validate_argument_syntax(args: Optional[list[str]] = None) -> ArgumentData:
    """
    Encapsulates Definition and Validation of Argument Syntax.
    Parses command line arguments.

    Parameters:
    - args: A list of argument strings.

    Returns:
    ArgumentData : Container for Valid Argument Data.
    """
    if args is None or len(args) == 0:
        raise SystemError("No Arguments given")
    # Initialize the Parser and Parse Immediately
    parsed_args = _define_arguments().parse_args(args)
    if parsed_args is None:
        raise ValueError("Arguments are Missing or Invalid.")
    # Validate Tree Name Syntax
    tree_file = parsed_args.tree_file
    if not _is_nonempty_str(tree_file):
        raise ValueError("The Tree File argument cannot be empty.")
    # Validate Data Directory Name Syntax if Present
    data_dir = parsed_args.data_dir
    if data_dir is not None:
        if not _is_nonempty_str(data_dir):
            raise ValueError("The Tree File argument cannot be empty.")
    # Return the Syntactically valid Argument Data
    return ArgumentData(
        tree_file,
        data_dir,
        is_reversed=parsed_args.reversed
    )


def _define_arguments() -> ArgumentParser:
    """
    Defines Command Line Requirements, Optional Arguments and Flags.

    Returns:
    argparse.ArgumentParser - An instance with all supported FTB Arguments.
    """
    parser = ArgumentParser(
        description="File Tree Builder"
    )
    # Required argument
    parser.add_argument(
        'tree_file',
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
        '--reverse',
        '-r',
        default=False,
        help='Flag to reverse the File Tree Operation'
    )
    return parser


def _is_nonempty_str(argument) -> bool:
    """
    Determine whether an argument is a non-empty string. Does not count whitespace.
    Uses the strip method to remove empty space.

    Parameters:
    - argument (str) : The given argument.

    Returns:
    bool - True if the argument is a non-empty (non-blank) string.
    """
    if argument is None or not isinstance(argument, str):
        return False
    elif len(argument.strip()) < 1:
        return False
    return True
