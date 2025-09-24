""" Tree Trimming Methods.
 Author: DK96-OS 2024 - 2025
"""
from typing import Callable

from treescript_builder.data.control_modes import WriteControlModes, TextMergeControlModes, ControlMode
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.operations import path_operations


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
    trim_method = _get_trimmer_method(control_mode, move_files)
    return tuple(_trim_instruction(i, trim_method) for i in instructions)


def _trim_instruction(
    instruct: InstructionData,
    trim_method: Callable[[InstructionData], bool],
) -> bool:
    """ Wraps the intersection of InstructionData and Trimmer Method.
 - Handles Directory instructions outside of Trimmer Method.

**Parameters:*
 - instruct (InstructionData): Data describing a trim operation step.
 - trim_method (Callable): A path_operation method, applied to all File Instructions.

**Returns:**
 bool - True if operation succeeds. False if OSError occurs, or trimmer method canceled file operation.
    """
    try:
        # Only Path in Instruction is required for directory.
        return path_operations.remove_empty_dir(instruct.path) \
            if instruct.is_dir else trim_method(instruct)
    except OSError:
        return False


def _get_trimmer_method(
    control_mode: ControlMode,
    move_files: bool,
) -> Callable[[InstructionData], bool]:
    if isinstance(control_mode, WriteControlModes):
        write_method = path_operations.get_overwrite_operation(move_files, control_mode.exact_build) \
            if control_mode.overwrite else \
            path_operations.get_trywrite_operation(move_files)
        return lambda i: write_method(i.data_path, i.path)
    elif isinstance(control_mode, TextMergeControlModes):
        text_merge_method = path_operations.get_text_merge_method(move_files, control_mode.prepend_merge)
        return lambda i: text_merge_method(i.data_path, i.path)
    else:
        raise ValueError(f'Unknown ControlMode of Type: {type(control_mode)}')
