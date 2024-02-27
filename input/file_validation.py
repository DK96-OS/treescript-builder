"""File Validation Methods.
"""
from typing import Optional
from pathlib import Path


def validate_input_file(file_name: str) -> str:
    """
    Read the Input File, Validate (non-blank) data, and return Input str.

    Parameters:
    - file_name (str): The Name of the Input File.

    Returns:
    str - The String Contents of the Input File.

    Raises:
    IOError - If the File does not exist, or is empty or blank.
    """
    file_path = Path(file_name)
    if not file_path.exists():
        raise IOError("The Input File does not Exist.")
    data = _get_input(file_path)
    if len(data) < 1:
        raise IOError("Input was Empty")
    return data


def validate_directory(dir_path_str: Optional[str]) -> Optional[Path]:
    """
    Ensure that if the Directory is present, it Exists.

    Parameters:
    - dir_path_str (str, optional): The String representation of the Path to the Directory.

    Returns:
    Path (optional) - The Directory Path, or None if given input is None.

    Raises:
    IOError - If the given path does not exist.
    """
    if dir_path_str is None:
        return None
    path = Path(dir_path_str)
    if path.exists():
        return path
    raise IOError("The given Directory does not exist!")


def _get_input(file: Path) -> str:
    """
    Read the String contents of the File, strips surrounding space characters.

    Parameters:
    - file (Path): The Path to the File.

    Returns:
    str - The text contents of the File at the given Path.

    Raises
    IOError - If the file does not exist, or the read operation failed.
    """
    if not file.exists():
        raise IOError("File does not exist.")
    try:
        return file.read_text().strip()
    except:
        raise IOError("Failed to Read from File.")
