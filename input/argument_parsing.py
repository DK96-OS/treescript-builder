"""Defines and Validates Argument Syntax.
    Encapsulates Definition and Validation of Argument Syntax.
"""
from argparse import ArgumentParser
from input.argument_data import ArgumentData
from typing import Optional


def parse_arguments(args: Optional[list[str]] = None) -> ArgumentData:
    """
    Parse command line arguments.

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
    tree_file_name = parsed_args.tree_file_name
    if not _is_nonempty_str(tree_file_name):
        raise ValueError("The Tree File argument cannot be empty.")
    # Validate Data Directory Name Syntax if Present
    data_dir_name = parsed_args.data_dir
    if data_dir_name is not None:
        if not _is_nonempty_str(data_dir_name):
            raise ValueError("The Tree File argument cannot be empty.")
    # Return the Syntactically valid Argument Data
    return ArgumentData(
        tree_file_name,
        data_dir_name,
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
        '--reverse',
        '-r',
        default=False,
        help='Flag to reverse the File Tree Operation'
    )
    return parser
