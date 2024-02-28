"""The Input Module.

1. Validate And Format Input Arguments.
2. Read Input Instructions.

"""
from data.input_data import InputData
from data.instruction_data import InstructionData


def validate_input_arguments(arguments: list[str]) -> InputData:
    """
    Parse and Validate the Arguments, then return as InputData.

    Parameters:
    - arguments (list[str]): The list of Arguments to validate.
    
    Returns:
    InputData - An InputData instance.

    Raises:
    ValueError - When Argument Syntax is Invalid.
    IOError - When given Input File or Directory does not exist.
    """
    from input.argument_validation import validate_argument_syntax
    from input.file_validation import validate_input_file, validate_directory
    arg_data = validate_argument_syntax(arguments)
    return InputData(
        validate_input_file(arg_data.input_file_path_str),
        validate_directory(arg_data.data_dir_path_str),
        arg_data.is_reversed
    )


def read_input_instructions(input_data: InputData) -> list[InstructionData]:
    """
    Process Multiple Lines from the Tree Node Structure Input.

    Parameters:
    - input_string (str): The Input containing multiple lines of tree node data.

    Returns:
    list[InstructionData] - The List of Instruction Data, read from the Input String.
    """
    from input.line_reader import process_line
    return [
        process_line(line) for line in input_data.tree_input.split("\n")
    ]
