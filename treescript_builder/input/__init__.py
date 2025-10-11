""" The Input Package Module.
 - Validate And Format Input Arguments.
 - Read Input TreeScript String from File.
 Author: DK96-OS 2024 - 2025
"""
from treescript_builder.data.input_data import InputData
from treescript_builder.input import argument_parser, file_validation, option_validation


def validate_input_arguments(
    arguments: list[str],
) -> InputData:
    """ Parse and Validate the Arguments, then return as InputData.

**Parameters:**
 - arguments (list[str]): The list of Arguments to validate.
    
**Returns:**
 InputData - An InputData instance.

**Raises:**
 SystemExit - If Arguments, Input File or Directory names invalid.
    """
    arg_data = argument_parser.parse_arguments(arguments)
    return InputData(
        tree_input=file_validation.validate_input_file(arg_data.input_file_path_str),
        data_dir=file_validation.validate_directory(arg_data.data_dir_path_str),
        trim_tree=arg_data.trim_tree,
        move_files=arg_data.move_files,
        control_mode=(control_mode := option_validation.get_control_modes_from_arg_data(arg_data)),
        verbosity_level=option_validation.get_verbosity_from_args(
            control_mode, arg_data.verbosity,
        ),
    )
