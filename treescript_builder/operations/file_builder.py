""" Tree Building Operations.
 Author: DK96-OS 2024 - 2025
"""
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
    build_method = _get_builder_method(control_mode, move_files)
    return tuple(_build_instruction(i, build_method) for i in instructions)


def _build_instruction(
    instruct: InstructionData,
    build_method: Callable[[InstructionData], bool],
) -> bool:
    """ Wraps the computational intersection of InstructionData and Builder Method.
 - Handles Directory instructions outside of Builder Method.

**Parameters:*
 - instruct (InstructionData): Data describing a build operation step.
 - build_method (Callable): A path_operation method, applied to all File Instructions.

**Returns:**
 bool - True if operation succeeds. False if OSError occurs, or builder method canceled file operation.
    """
    try:
        # Only Path in Instruction is required for directory.
        return path_operations.make_dir_exist(instruct.path)\
            if instruct.is_dir else build_method(instruct) 
    except OSError:
        return False


def _get_builder_method(
    control_mode: ControlMode,
    move_files: bool,
) -> Callable[[InstructionData], bool]:
    if isinstance(control_mode, WriteControlModes):
        write_method = path_operations.get_overwrite_operation(move_files, control_mode.exact_build) \
            if control_mode.overwrite else \
            path_operations.get_trywrite_operation(move_files)
        return lambda i: write_method(i.path, i.data_path)
    elif isinstance(control_mode, TextMergeControlModes):
        text_merge_method = path_operations.get_text_merge_method(move_files, control_mode.prepend_merge)
        return lambda i: text_merge_method(i.path, i.data_path)
    else:
        raise ValueError(f'Unknown ControlMode of Type: {type(control_mode)}')
