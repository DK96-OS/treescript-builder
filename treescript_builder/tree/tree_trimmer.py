""" Tree Trimming Methods.
 Author: DK96-OS 2024 - 2025
"""
from typing import Callable

from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.path_operations import prepend_to_file, append_to_file, overwrite_file, extract_file


def trim(
    instructions: tuple[InstructionData, ...],
    mode: FileModeEnum,
) -> tuple[bool, ...]:
    """ Trim a File Tree using the Instructions in the given File Mode.

**Parameters:**
 - instructions(tuple[InstructionData, ...]): The Instructions containing File Tree information and Data paths.
 - mode (FileModeEnum): The type of modification to apply with existing file contents.

**Returns:**
 tuple[bool, ...] - The success or failure of each instruction.
    """
    trim_method = _get_trimmer_method(mode)
    return tuple(_trim_instruction(i, trim_method) for i in instructions)


def _trim_instruction(
    instruct: InstructionData,
    trim_method: Callable[[InstructionData], bool],
) -> bool:
    if instruct.data_path is not None:
        return trim_method(instruct)
    try:
        if instruct.is_dir:
            instruct.path.rmdir()
        else:
            instruct.path.unlink(missing_ok=True)
    except OSError:
        return False
    return True


def _get_trimmer_method(
    mode: FileModeEnum,
) -> Callable[[InstructionData], bool]:
    match mode:
        case FileModeEnum.APPEND:
            return lambda i: append_to_file(i.data_path, i.path)
        case FileModeEnum.CANCEL:
            return lambda i: extract_file(i.data_path, i.path)
        case FileModeEnum.OVERWRITE:
            return lambda i: overwrite_file(i.data_path, i.path)
        case FileModeEnum.PREPEND:
            return lambda i: prepend_to_file(i.data_path, i.path)
        case _:
            exit()
