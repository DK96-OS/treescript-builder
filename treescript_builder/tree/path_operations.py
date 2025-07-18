""" File Tree Operations.
 - These methods perform File System operations using Path objects.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from shutil import copy2


def make_dir_exist(
    path: Path
) -> bool:
    """ Ensure that the Directory at the given Path exists.

**Parameters:**
 - path (Path): The Path to the File to be created, and written to.

**Returns:**
 bool - True if the Operation Succeeded, or if the Path already exists.
    """
    if path.exists():
        return True
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False
    return True


def append_to_file(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    """ Append to the end of the file.

**Parameters:**
 - path (Path): The Path to the file to be appended to.
 - data (Path): A Data Directory File Path to copy from.

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
    """ Prepend, adding text to the start of the file.

**Parameters:**
 - path (Path): The Path to the file to be appended to.
 - data (Path): A Data Directory File Path to copy from.
 
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

**Parameters:**
 - path (Path): The Path to the File to be created, and written to.
 - data (Path): A Data Directory Path to be copied to the new File.

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
