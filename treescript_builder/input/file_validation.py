""" File Validation Methods.
 - These Methods all raise SystemExit exceptions.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from sys import exit

from treescript_builder.input.string_validation import validate_name

_FILE_SIZE_LIMIT = 32 * 1024 # 32 KB
_FILE_SIZE_LIMIT_ERROR_MSG = "File larger than 32 KB Limit."
_FILE_SYMLINK_DISABLED_MSG = "Symlink file paths are disabled."

_FILE_DOES_NOT_EXIST_MSG = "The File does not Exist."
_FILE_READ_OSERROR_MSG = "Failed to Read from File."
_FILE_VALIDATION_ERROR_MSG = "Invalid Input File Contents."

_NOT_A_DIR_ERROR_MSG = "Not a Directory."
_DIR_DOES_NOT_EXIST_MSG = "The Directory does not exist."

_TEXT_FILE_SIZE_LIMIT = 2 * 1024**2 # 2 MB
_TEXT_FILE_SIZE_LIMIT_ERROR_MSG = "Text File larger than 2 MB Limit."


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
    if not validate_name(data := safe_read_text_file(Path(file_name), file_size_limit=_FILE_SIZE_LIMIT)):
        exit(_FILE_VALIDATION_ERROR_MSG)
    return data


def validate_directory(
    dir_path_str: str | None,
) -> Path | None:
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
        exit(_NOT_A_DIR_ERROR_MSG)
    exit(_DIR_DOES_NOT_EXIST_MSG)


def safe_read_text_file(
    file_path: Path,
    file_size_limit: int = _TEXT_FILE_SIZE_LIMIT,
) -> str:
    """ Safely read a TextFile from a Path.
 - Designed for use in Text Merge Operations, where text files are read and appended.
 - Quickly returns empty string if the file is missing.
 - Exits if a real issue with the file is found: symlink, over 4 MB size limit.
    """
    try:
        if not check_not_symlink(file_path):
            return ''
        if file_path.lstat().st_size > file_size_limit:
            exit(_TEXT_FILE_SIZE_LIMIT_ERROR_MSG)
        return file_path.read_text()
    except OSError:
        exit(_FILE_READ_OSERROR_MSG)
    return ''


def check_not_symlink(file_path: Path) -> bool:
    return (not file_path.is_symlink()) and file_path.exists()


def check_text_file_stats(file_path: Path) -> bool:
    """ Check that the files are not too large for safer operations.
    """
    return check_not_symlink(file_path) and file_path.lstat().st_size <= _TEXT_FILE_SIZE_LIMIT
