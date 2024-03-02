"""The Input Module.

1. Validate And Format Input Arguments.
2. Read Input Tree.

"""
from typing import Generator
from itertools import groupby
from data.input_data import InputData
from data.tree_data import TreeData
from input.line_reader import process_line


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


def read_input_tree(input_data: InputData) -> tuple[TreeData, ...]:
    """
    Process Multiple Lines from the Tree Node Structure Input.

    Parameters:
    - input_data (InputData): The Input containing multiple lines of tree node data.

    Returns:
    tuple[InstructionData] - The Tuple of Instruction Data, read from the Input String.
    """
    return (
        process_line(line) for line in input_data.tree_input.split("\n")
    )


def tree_node_generator(input_data: InputData) -> Generator[TreeData, None, None]:
    """
    Generate structured Tree Data from the Input Data String.

    Parameters:
    - input_data (InputData): The Input.

    Returns:
    Generator[TreeData] - 
    """
    for is_newline, group in groupby(input_data.tree_input, lambda x: x == "\n"):
        if not is_newline:
            yield process_line(''.join(group))
