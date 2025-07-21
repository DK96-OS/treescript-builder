""" File Tree Operations.
 - These methods perform File System operations using Path objects.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from shutil import copy2


def make_dir_exist(
    dir_path: Path,
) -> bool:
    """ Ensure that the Directory at the given Path exists.
 - Creates Parent Directories when necessary.

**Parameters:**
 - dir_path (Path): The Path to the Directory (and parent directories) to be created.

**Returns:**
 bool - True if the Operation Succeeded, and the directory now exists.
    """
    try:
        if dir_path.exists():
            return True
        dir_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False
    return True


def append_to_file(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    """ Append data, adds text to the end of the target file.
 - If source_file is none, creates the target file if it doesn't exist.

**Parameters:**
 - target_file (Path): The Path to the file to be appended to.
 - source_file (Path?): A Data Directory File Path to read text data from.

**Returns:**
 bool - Whether the File operation succeeded.
    """
    try:
        if source_file is None:
            target_file.touch(exist_ok=True)
            return True
        source_file_content = source_file.read_text()
        with target_file.open('a') as f:
            f.write(source_file_content)
    except OSError:
        return False
    return True


def prepend_to_file(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    """ Prepend data, adds text to the start of the target file.
 - If source_file is none, creates the target file if it doesn't exist.

**Parameters:**
 - target_file (Path): The Path to the file to be appended to.
 - source_file (Path?): A Data Directory File Path to read text data from.
 
**Returns:**
 bool - Whether the File operation succeeded.
    """
    try:
        if source_file is None:
            target_file.touch(exist_ok=True)
            return True
        target_file_content = target_file.read_text()
        data_file_content = source_file.read_text()
        with target_file.open('w') as f:
            f.write(data_file_content)
            f.write(target_file_content)
    except OSError:
        return False
    return True


def overwrite_file(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    """ Create or overwrite a File at the given path, with data from the Data Directory source file.
 - If source_file is none, creates the file if it does not exist.

**Parameters:**
 - target_file (Path): The Path to the File to be created, and written to.
 - source_file (Path?): A Data Directory File Path to be copied, overwriting the target File.

**Returns:**
 bool - Whether the File operation succeeded.
    """
    try:
        if source_file is None:
            target_file.touch(exist_ok=True)
        else:
            copy2(source_file, target_file)
    except OSError:
        return False
    return True
