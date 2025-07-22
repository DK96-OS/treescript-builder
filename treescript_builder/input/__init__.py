""" The Input Module.
 - Validate And Format Input Arguments.
 - Read Input Tree String from File.
 Author: DK96-OS 2024 - 2025
"""
from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.input.argument_data import ArgumentData
from treescript_builder.input.argument_parser import parse_arguments
from treescript_builder.input.file_validation import validate_input_file, validate_directory
from treescript_builder.input.input_data import InputData


def validate_input_arguments(arguments: list[str]) -> InputData:
    """ Parse and Validate the Arguments, then return as InputData.

**Parameters:**
 - arguments (list[str]): The list of Arguments to validate.
    
**Returns:**
 InputData - An InputData instance.

**Raises:**
 SystemExit - If Arguments, Input File or Directory names invalid.
    """
    arg_data = parse_arguments(arguments)
    return InputData(
        tree_input=validate_input_file(arg_data.input_file_path_str),
        data_dir=validate_directory(arg_data.data_dir_path_str),
        is_reversed=arg_data.is_reversed,
        mode=_determine_file_mode_from_arg_data(arg_data),
    )


def _determine_file_mode_from_arg_data(
    arg_data: ArgumentData,
) -> FileModeEnum:
    if arg_data.prepend:
        return FileModeEnum.PREPEND
    elif arg_data.overwrite:
        return FileModeEnum.OVERWRITE
    return FileModeEnum.APPEND
