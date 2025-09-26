""" Tree Building Operations.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from typing import Callable

from treescript_builder.data.control_modes import WriteControlModes, TextMergeControlModes, ControlMode
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.operations import path_operations


def build(
    instructions: tuple[InstructionData, ...],
    move_files: bool,
    control_mode: ControlMode,
) -> tuple[bool, ...]:
    """ Build a File Tree from the InstructionData, applying given Control Mode options.

**Parameters:**
 - instructions(tuple[InstructionData]): The File Tree and Data Instructions to build with.
 - move_files (bool): Whether files should be moved instead of copied to the target destination.
 - control_mode (ControlMode): The options controlling the details of the build operations.

**Returns:**
 tuple[bool, ...] - The result (success or failure) of each instruction.
    """
    if not isinstance(instructions, tuple) or \
            not isinstance(move_files, bool) or \
            not isinstance(control_mode, ControlMode):
        raise TypeError
    path_method = _get_path_method(control_mode, move_files)
    instruct_method = lambda x: path_method(x.path, x.data_path)
    return tuple(_build_instruction(i, instruct_method) for i in instructions)


def trim(
    instructions: tuple[InstructionData, ...],
    move_files: bool,
    control_mode: ControlMode,
) -> tuple[bool, ...]:
    """ Trim a File Tree using the Instructions, applying given Control Mode options.

**Parameters:**
 - instructions(tuple[InstructionData, ...]): The File Tree and Data Instructions to trim with.
 - move_files (bool): Whether files should be moved instead of copied to the target destination.
 - control_mode (ControlMode): The options controlling the details of the trim operations.

**Returns:**
 tuple[bool, ...] - The result (success or failure) of each instruction.
    """
    if not isinstance(instructions, tuple) or \
            not isinstance(move_files, bool) or \
            not isinstance(control_mode, ControlMode):
        raise TypeError
    path_method = _get_path_method(control_mode, move_files)
    instruct_method = lambda x: path_method(x.data_path, x.path)
    return tuple(_trim_instruction(i, instruct_method) for i in instructions)


def _build_instruction(
    instruct: InstructionData,
    build_method: Callable[[InstructionData], bool],
) -> bool:
    """ Wraps the computational intersection of InstructionData and Builder Method.
 - Handles Directory instructions outside of Builder Method.

**Parameters:*
 - instruct (InstructionData): Data describing a build operation step.
 - build_method (Callable): A path_operation method, applied to File Instructions.

**Returns:**
 bool - True if operation succeeds. False if OSError occurs, or builder method canceled file operation.
    """
    try:
        # Only Path in Instruction is required for directory.
        return path_operations.make_dir_exist(instruct.path)\
            if instruct.is_dir else build_method(instruct) 
    except OSError:
        return False


def _trim_instruction(
    instruct: InstructionData,
    trim_method: Callable[[InstructionData], bool],
) -> bool:
    """ Wraps the intersection of InstructionData and Trimmer Method.
 - Handles Directory instructions outside of Trimmer Method.

**Parameters:*
 - instruct (InstructionData): Data describing a trim operation step.
 - trim_method (Callable): A path_operation method, applied to File Instructions.

**Returns:**
 bool - True if operation succeeds. False if OSError occurs, or trimmer method canceled file operation.
    """
    try:
        # Only Path in Instruction is required for directory.
        return path_operations.remove_empty_dir(instruct.path) \
            if instruct.is_dir else trim_method(instruct)
    except OSError:
        return False


def _get_path_method(
    control_mode: ControlMode,
    move_files: bool,
) -> Callable[[Path, Path | None], bool]:    
    if isinstance(control_mode, WriteControlModes):
        return path_operations.get_write_operation(move_files, control_mode.overwrite, control_mode.exact_build)
    elif isinstance(control_mode, TextMergeControlModes):
        return path_operations.get_text_merge_method(move_files, control_mode.prepend_merge)
    else:
        raise TypeError(f'Unknown ControlMode of Type: {type(control_mode)}')
