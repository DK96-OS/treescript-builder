""" File Validation Methods.
 - These Methods all raise SystemExit exceptions.
 Author: DK96-OS 2024 - 2025
"""
from os.path import normpath, abspath
from pathlib import Path
from sys import exit

from treescript_builder.input.string_validation import validate_name


def validate_input_file(file_name: str) -> str | None:
    """ Read the Input File, Validate (non-blank) data, and return Input str.

**Parameters:**
 - file_name (str): The Name of the Input File.

**Returns:**
 str - The String Contents of the Input File.

**Raises:**
 SystemExit - If the File does not exist, or is empty or blank, or read failed.
    """
    if not (file_path := Path(_normalize_pathname(file_name))).exists():
        exit(f"The Input File does not Exist: {str(file_path)}")
    try:
        if (data := file_path.read_text()) is not None and validate_name(data):
            return data
    except OSError as e:
        exit(f"Failed to Read from File: {e}")
    return None


def validate_directory(
    dir_path_str: str | None,
) -> Path | None:
    """ Ensure that if the Directory is present, it Exists.

**Parameters:**
- dir_path_str (str?): The String representation of the Path to the Directory.

**Returns:**
 Path? - The DataDirectory Path, or None if given input is None.

**Raises:**
 SystemExit - If a given path does not exist.
    """
    if dir_path_str is None:
        return None # DataDirectory is optional. Return None before _normalize_pathname raises typeerror.
    if not validate_name(dir_path_str):
        exit("Data Directory is invalid")
    if (path := Path(_normalize_pathname(dir_path_str))).exists():
        return path
    exit("The given Directory does not exist!")


def _normalize_pathname(path_name: str | None) -> str:
    if path_name is None or not isinstance(path_name, str):
        raise TypeError
    return normpath(str(Path(path_name).expanduser()))
