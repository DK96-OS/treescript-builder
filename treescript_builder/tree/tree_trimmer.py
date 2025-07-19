""" Tree Trimming Methods.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from shutil import move
from typing import Callable

from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.data.instruction_data import InstructionData


def trim(
    instructions: tuple[InstructionData, ...],
    mode: FileModeEnum,
) -> tuple[bool, ...]:
    """ Trim a File Tree using the Instructions in the given File Mode.

**Parameters:**
 - instructions(tuple[InstructionData]): The Instructions containing File Tree information and Data paths.
 - mode (FileModeEnum): The type of modification to apply with existing file contents.

**Returns:**
 tuple[bool, ...] - The success or failure of each instruction.
    """
    trim_method = _get_trimmer_method(mode)
    return tuple(
        trim_method(i)
        for i in instructions
    )


def _get_trimmer_method(
    mode: FileModeEnum,
) -> Callable[[InstructionData], bool]:
    match mode:
        case FileModeEnum.APPEND:
            return _trim
        case FileModeEnum.OVERWRITE:
            return _trim
        case FileModeEnum.PREPEND:
            return _trim
        case _:
            exit()


def _trim(instruct: InstructionData) -> bool:
    if instruct.is_dir:
        return _remove_dir(instruct.path)
    if instruct.data_path is None:
        try:
            instruct.path.unlink(missing_ok=True)
        except OSError:
            return False
        return True
    return _extract_file(instruct.path, instruct.data_path)


def _extract_file(
    path: Path,
    data: Path
) -> bool:
    """ Moves the File to the Data Directory.

**Parameters:**
 - path (Path): The path to the File in the Tree.
 - data (Path): A Path to a File in the Data Directory.

**Returns:**
 bool - Whether the entire operation succeeded.
    """
    try:
        move(path, data)
    except OSError:
        return False
    return True


def _remove_dir(
    path: Path,
) -> bool:
    """ Tries to Remove a Directory, if it is Empty.

**Parameters:**
 - path (Path): The path to the Directory.

**Returns:**
 bool - Whether the Directory was Empty, and has been removed.
    """
    try:
        path.rmdir()
    except OSError:
        return False
    return True