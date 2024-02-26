"""Gather and Validate the Input.
"""
from typing import Optional
from pathlib import Path
from input.argument_data import ArgumentData
from input_data import InputData


def validate_tree_input(tree_file_name: str) -> str:
    """Ensure that the Tree Input File Exists and Contains non-empty data.

    Parameters:
    - tree_file_name (str): The Name of the Tree Input File.

    Returns:
    str - The String Contents of the Tree Input File.
    
    Throws:
    IOError - If the File does not exist, or is empty (or blank).
    """
    tree_file_path = Path(tree_file_name)
    if not tree_file_path.exists():
        raise IOError("The Tree Input File does not Exist.")
    data = tree_file_path.read_text().strip()
    if len(data) < 1:
        raise IOError("Tree Input was Empty")
    return data


def get_tree_input(tree_file: Path) -> str:
    """Obtain the String contents of the Tree File."""
    if not tree_file.exists():
        raise IOError("Tree File does not exist.")
    try:
        return tree_file.read_text()
    except:
        raise IOError("Failed to Read from Tree File.")


def validate_data_directory(data_dir_path_str: Optional[str]) -> Optional[Path]:
    """Ensure that if the Data Directory is present, it Exists.

    Parameters:
    - data_dir_path_str (str, optional) : The String representation of the Path to the Data Directory.

    Returns:
    Path - The Data Directory Path.

    Throws:
    IOError - If the given path does not exist.
    """
    if data_dir_path_str is None:
        return None
    else:
        data_dir = Path(data_dir_path_str)
        if not data_dir.exists():
            raise IOError("The given Data Directory does not exist!")
        return data_dir


def validate_input_data(arg_data: ArgumentData) -> InputData:
    """
    """
    return InputData(
        validate_tree_input(arg_data.input_file_path_str),
        validate_data_directory(arg_data.data_dir_path_str),
        arg_data.is_reversed
    )


def get_input_from_args(arguments: list[str]) -> InputData:
    """Parse and Validate the Arguments, then return as InputData.

    Parameters:
    - arguments (list[str]) : The list of Arguments to validate.
    
    Returns:
    InputData - An InputData instance.

    Throws:
    ValueError - When Argument Syntax is Invalid.
    IOError - When given Input File or Directory does not exist.
    """
    from input.argument_validation import validate_argument_syntax
    return validate_input_data(validate_argument_syntax(arguments))
