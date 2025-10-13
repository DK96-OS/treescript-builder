""" File Tree Operations.
 - These methods perform File System operations using Path objects.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from shutil import copy2, move
from typing import Callable


def make_dir_exist(
    dir_path: Path,
) -> bool:
    """ Ensure that the Directory at the given Path exists.
 - Creates Parent Directories when necessary.

**Parameters:**
 - dir_path (Path): The Path to the Directory (and parent directories) to be created.

**Returns:**
 bool - True if the Operation Succeeded, and the directory now exists. False if error occurred.
    """
    try:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except OSError:
        return False


def remove_empty_dir(
    dir_path: Path,
) -> bool:
    """ Try to remove a Directory at the given Path.
 - Note that directories can only be removed if empty. This aligns with target TreeScript trim behavior.

**Parameters:**
 - dir_path (Path): The path to the directory to try to remove.

**Returns:**
 bool - True of the directory was removed successfully, false if it was non-empty, or the Path was not a Dir.
    """
    try: 
        dir_path.rmdir()
    except OSError:
        return False
    return True


def get_trywrite_operation(
    move_file: bool,
) -> Callable[[Path, Path | None], bool]:
    """ Obtain the Operation that checks the TargetFile before writing to it.
 - These operations yield when TargetFile is non-empty.

**Parameters:**
 - move_file (bool): Whether to move the file, instead of copy.

**Returns:**
 Callable[[Path, Path?], bool] - A Method that operates on Paths.
    """
    return _try_move if move_file else _try_copy


def get_overwrite_operation(
    move_file: bool,
    exact: bool,
) -> Callable[[Path, Path | None], bool]:
    """ Obtain the Operation that Overwrites the TargetFile with the SourceFile.
- If not exact, the TargetFile won't be overwritten if SourceFile is empty.
- Exactness feature is added to help protect against accidental overwrites.

**Parameters:**
 - move_file (bool): Whether to move the file, instead of copy.
 - exact (bool): Whether operation should follow exact builder instructions, or yield when SourceFile is empty. Default: False.

**Returns:**
 Callable[[Path, Path?], bool] - A Method that operates on Paths.
    """
    return (_ow_exact_move if exact else _ow_move) if move_file else (_ow_exact_copy if exact else _ow_copy)


def get_write_operation(
    move_file: bool,
    overwrite: bool,
    exact: bool,
) -> Callable[[Path, Path | None], bool]:
    """ Obtain a Path Operation Method for the Write Mode (not TextMerge Mode).
 - Includes TryWrite and Overwrite Methods.
 - See other similar methods for more details: get_trywrite_operation, get_overwrite_operation.

**Parameters:**
 - move_file (bool): Whether to move the file, instead of copy.
 - overwrite (bool): Whether to overwrite files, instead of checking for contents before writing.
 - exact (bool): Whether operation should follow exact builder instructions, or yield when SourceFile is empty.

**Returns:**
 Callable[[Path,Path?], bool] - The Path Operations method that matches the parameters.
    """
    return get_overwrite_operation(move_file, exact) if overwrite else get_trywrite_operation(move_file)


def get_text_merge_method(
    move_file: bool,
    prepend: bool,
) -> Callable[[Path, Path | None], bool]:
    """ Obtain a Path Operation Method that Merges TargetFile and SourceFile Texts.

**Parameters:**
 - move_file (bool): Whether to move the file, instead of copy.
 - prepend (bool): Whether the TextMode is Prepend. The other Mode is Append.

**Returns:**
 Callable[[Path, Path?], bool] - A Method that operates on Paths objects.
    """
    return (_prepend_move if move_file else _prepend_copy) \
        if prepend else \
        (_append_move if move_file else _append_copy)


def _is_non_empty_path(
    target_file: Path,
) -> bool:
    try:
        return target_file.exists() and target_file.stat().st_size > 0
    except OSError:
        # The purpose of this method is trying to prevent overwrite.
        return True # True will likely cancel the Operation.


def _try_copy(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if _is_non_empty_path(target_file):
        return False
    copy2(source_file, target_file)
    return True


def _try_move(
    target_file: Path,
    source_file: Path,
) -> bool:
    if _is_non_empty_path(target_file):
        return False
    move(source_file, target_file)
    return True


def _ow_copy(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if source_file is None:
        target_file.touch(exist_ok=True)
    else:
        copy2(source_file, target_file)
    return True


def _ow_move(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if source_file is None:
        target_file.touch(exist_ok=True)
    else:
        move(source_file, target_file)
    return True


def _ow_exact_copy(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if source_file is None:
        target_file.touch(exist_ok=True)
    else:
        copy2(source_file, target_file)
    return True


def _ow_exact_move(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    move(source_file, target_file)
    return True


def _append_copy(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if source_file is None:
        target_file.touch(exist_ok=True)
        return True
    src_contents = source_file.read_text()
    with target_file.open('a') as f:
        f.write(src_contents)
    return True


def _append_move(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if source_file is None:
        target_file.touch(exist_ok=True)
        return True
    src_contents = source_file.read_text()
    with target_file.open('a') as f:
        f.write(src_contents)
    source_file.unlink() # Remove src File, as it is being 'moved'.
    return True


def _prepend_copy(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if source_file is None:
        target_file.touch(exist_ok=True)
        return True
    target_contents = target_file.read_text()
    src_contents = source_file.read_text()
    with target_file.open('w') as f:
        f.write(src_contents)
        f.write(target_contents)
    return True


def _prepend_move(
    target_file: Path,
    source_file: Path | None,
) -> bool:
    if source_file is None:
        target_file.touch(exist_ok=True)
        return True
    target_contents = target_file.read_text()
    src_file_content = source_file.read_text()
    with target_file.open('w') as f:
        f.write(src_file_content)
        f.write(target_contents)
    source_file.unlink()
    return True
