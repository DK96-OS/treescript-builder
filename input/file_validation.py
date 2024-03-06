"""File Validation Methods.
    These Methods all raise SystemExit exceptions.
"""
from pathlib import Path
from sys import exit
from typing import Optional

from input.string_validation import validate_name


def validate_input_file(file_name: str) -> str:
    """
    Read the Input File, Validate (non-blank) data, and return Input str.

    Parameters:
    - file_name (str): The Name of the Input File.

    Returns:
    str - The String Contents of the Input File.

    Raises:
    SystemExit - If the File does not exist, or is empty or blank.
    """
    file_path = Path(file_name)
    if not file_path.exists():
        exit("The Input File does not Exist.")
    data = _get_input(file_path)
    if validate_name(data):
        return data
    exit("Input was Empty")


def validate_directory(dir_path_str: Optional[str]) -> Optional[Path]:
    """
    Ensure that if the Directory is present, it Exists.

    Parameters:
    - dir_path_str (str, optional): The String representation of the Path to the Directory.

    Returns:
    Path (optional) - The Directory Path, or None if given input is None.

    Raises:
    SystemExit - If the given path does not exist.
    """
    if dir_path_str is None:
        return None
    if not validate_name(dir_path_str):
        exit("Data Directory is invalid")
    path = Path(dir_path_str)
    if path.exists():
        return path
    exit("The given Directory does not exist!")


def get_file_extension(file_name: str) -> Optional[str]:
    """
    Obtain the File Extension, if it exists.
        The Last extension in a multi-part extension is returned.
    
    Parameters:
    - file_name (str): The name of the File.

    Returns:
    str or None - The File Extension, or None.
    """
    try:
        index = file_name[::-1].index('.')
        result = file_name[len(file_name) - index:]
        if len(result) < 1:
            return None
        return result
    except:
        return None


def _get_input(file: Path) -> str:
    """
    Read the String contents of the File, strips surrounding space characters.

    Parameters:
    - file (Path): The Path to the File.

    Returns:
    str - The text contents of the File at the given Path.

    Raises
    SystemExit - If the file does not exist, or the read operation failed.
    """
    if not file.exists():
        exit("File does not exist.")
    try:
        return file.read_text().strip()
    except IOError as e:
        exit("Failed to Read from File.")
