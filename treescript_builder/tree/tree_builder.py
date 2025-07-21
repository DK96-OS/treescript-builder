""" Tree Building Operations.
 Author: DK96-OS 2024 - 2025
"""
from typing import Callable

from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.path_operations import prepend_to_file, overwrite_file, append_to_file, make_dir_exist


def build(
    instructions: tuple[InstructionData, ...],
    mode: FileModeEnum = FileModeEnum.OVERWRITE,
) -> tuple[bool, ...]:
    """ Build a File Tree from the Instructions in the given Mode.
 - This Method has a default mode of Overwrite.

**Parameters:**
 - instructions(tuple[InstructionData]): The Instructions to execute.
 - mode (FileModeEnum): The type of modification to apply with existing file contents. Default: Overwrite.

**Returns:**
 tuple[bool, ...] - The success or failure of each instruction.
    """
    build_method = _get_builder_method(mode)
    return tuple(_build_instruction(i, build_method) for i in instructions)


def _build_instruction(
    instruct: InstructionData,
    build_method: Callable[[InstructionData], bool],
) -> bool:
    if instruct.data_path is not None:
        return build_method(instruct)
    if instruct.is_dir:
        return make_dir_exist(instruct.path)
    try:    
        instruct.path.touch(exist_ok=True)
    except OSError:
        return False
    return True


def _get_builder_method(
    mode: FileModeEnum,
) -> Callable[[InstructionData], bool]:
    match mode:
        case FileModeEnum.APPEND:
            return _append
        case FileModeEnum.OVERWRITE:
            return _overwrite
        case FileModeEnum.PREPEND:
            return _prepend
        case _:
            exit()


def _append(
    instruct: InstructionData,
) -> bool:
    """ Execute a single instruction in append mode.

**Parameters:**
 - instruct(InstructionData): The data required to execute the operation. 

**Returns:**
 bool - Whether the given operation succeeded.
    """
    if instruct.data_path is None:
        instruct.path.touch(exist_ok=True)
        return True
    return append_to_file(instruct.path, instruct.data_path)


def _overwrite(
    instruct: InstructionData,
) -> bool:
    """ Execute a single instruction in overwrite mode.

**Parameters:**
 - instruct(InstructionData): The data required to execute the operation. 

**Returns:**
 bool - Whether the given operation succeeded.
    """
    if instruct.data_path is None:
        instruct.path.touch(exist_ok=True)
        return True
    return overwrite_file(instruct.path, instruct.data_path)


def _prepend(
    instruct: InstructionData,
) -> bool:
    """ Execute a single instruction in overwrite mode.

**Parameters:**
 - instruct(InstructionData): The data required to execute the operation. 

**Returns:**
 bool - Whether the File operation succeeded.
    """
    if instruct.data_path is None:
        instruct.path.touch(exist_ok=True)
        return True
    return prepend_to_file(instruct.path, instruct.data_path)
