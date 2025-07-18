""" Tree Building Operations.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from typing import Callable

from treescript_builder.data.file_mode_enum import FileModeEnum
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree.path_operations import prepend_to_file, overwrite_file, append_to_file, make_dir_exist


def build(
    instructions: tuple[InstructionData, ...],
    mode: FileModeEnum,
) -> tuple[bool, ...]:
    """ Execute the Instructions in build mode.

**Parameters:**
 - instructions(tuple[InstructionData]): The Instructions to execute.
 - mode (FileModeEnum): 

**Returns:**
 tuple[bool] - The success or failure of each instruction.
    """
    build_method = _get_builder_method(mode)
    return tuple(
        make_dir_exist(i.path) if i.is_dir else (
            i.path.touch(exist_ok=True) if i.data_path is None else build_method(i)
        )
        for i in instructions
    )


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


def _make_dir_exist(
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
