""" File Validation Methods.
 - These Methods all raise SystemExit exceptions.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from stat import S_ISLNK
from sys import exit

from treescript_builder.input.string_validation import validate_name


def validate_input_file(file_name: str) -> str | None:
    """ Read the Input File, Validate (non-blank) data, and return Input str.
 - Max FileSize is 32 KB.
 - Symlink type file paths are disabled.

**Parameters:**
 - file_name (str): The Name of the Input File.

**Returns:**
 str - The String Contents of the Input File.

**Raises:**
 SystemExit - If the File does not exist, or is empty, blank, over 32 KB, or if the read or validation operation failed.
    """
    file_path = Path(file_name)
    if not file_path.exists():
        exit("The File does not Exist.")
    try:
        if S_ISLNK((stat := file_path.lstat()).st_mode):
            exit("Symlink file paths are disabled.")
        elif stat.st_size > 32 * 1024**2: # 32 KB Limit
            exit("Input File is Larger than the 32 KB Limit.")
        if (data := file_path.read_text()) is not None:
            if validate_name(data):
                return data
            exit("Invalid Input File Contents.")
    except OSError:
        exit("Failed to Read from File.")
    return None


def validate_directory(dir_path_str: str | None) -> Path | None:
    """ Ensure that if the Directory argument is present, it Exists.
 - Allows None to pass through the method.

**Parameters:**
 - dir_path_str (str?): The String representation of the Path to the Directory.

**Returns:**
 Path? - The Path to the DataDirectory, or None if given input is None.

**Raises:**
 SystemExit - If a given path does not exist, or is not a Directory.
    """
    if dir_path_str is None:
        return None
    if (path := Path(dir_path_str)).exists():
        if path.is_dir():
            return path
        exit("Not a Directory.")
    exit("The Directory does not exist.")
