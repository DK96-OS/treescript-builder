"""The Input Module.
    Validate And Format Input Arguments.
    Read Input Tree String from File.
"""
from input.input_data import InputData
from input.argument_parser import parse_arguments
from input.file_validation import validate_input_file, validate_directory


def validate_input_arguments(arguments: list[str]) -> InputData:
    """
    Parse and Validate the Arguments, then return as InputData.

    Parameters:
    - arguments (list[str]): The list of Arguments to validate.
    
    Returns:
    InputData - An InputData instance.

    Raises:
    SystemExit - If Arguments, Input File or Directory names invalid.
    """
    arg_data = parse_arguments(arguments)
    return InputData(
        validate_input_file(arg_data.input_file_path_str),
        validate_directory(arg_data.data_dir_path_str),
        arg_data.is_reversed
    )
