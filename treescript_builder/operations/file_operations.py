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
    is_trim: bool,
    control_mode: ControlMode,
) -> tuple[bool, ...]:
    """ Build a File Tree from the InstructionData, applying given Control Mode options.
 - Combined with Trim FileOperation for a simpler module, where it is easier to see the difference between the operations.

**Parameters:**
 - instructions(tuple[InstructionData]): The File Tree and Data Instructions to build with.
 - move_files (bool): Whether files should be moved instead of copied to the target destination.
 - is_trim (bool): Whether the operation is Trim, rather than Build.
 - control_mode (ControlMode): The options controlling the details of the build operations.

**Returns:**
 tuple[bool, ...] - The result (success or failure) of each instruction.
    """
    if not isinstance(instructions, tuple) or \
            not isinstance(move_files, bool) or \
            not isinstance(is_trim, bool) or \
            not isinstance(control_mode, ControlMode):
        raise TypeError
    return _build_files(
        move_files, control_mode, instructions
    ) if not is_trim else _trim_files(
        move_files, control_mode, instructions
    )


def _build_files(
    move_files: bool,
    control_mode: ControlMode,
    instructions: tuple[InstructionData, ...],
) -> tuple[bool, ...]:
    path_method = _get_path_method(control_mode, move_files)
    return tuple(_build_instruction(
        instruct=i,
        # The DataFile is the SourcePath for Build Operations
        build_method=lambda x: path_method(x.path, x.data_path)
    ) for i in instructions)


def _trim_files(
    move_files: bool,
    control_mode: ControlMode,
    instructions: tuple[InstructionData, ...],
) -> tuple[bool, ...]:
    path_method = _get_path_method(control_mode, move_files)
    exact_build = control_mode.exact_build if isinstance(control_mode, WriteControlModes) else None
    return tuple(_trim_instruction(
        instruct=i,
        # The TargetFile is the SourcePath for Trim Operations
        trim_method=lambda x: path_method(x.data_path, x.path),
        move_files=move_files,
        exact=exact_build,
    ) for i in instructions)


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
    try: # Only Path in Instruction is required for directory.
        if instruct.is_dir:
            return path_operations.make_dir_exist(instruct.path)
        elif instruct.data_path is None:
            instruct.path.touch(exist_ok=True)
        else:
            return build_method(instruct)
    except OSError:
        return False
    except SystemExit:
        return False
    return True


def _trim_instruction(
    instruct: InstructionData,
    trim_method: Callable[[InstructionData], bool],
    move_files: bool,
    exact: bool
) -> bool:
    """ Wraps the intersection of InstructionData and Trimmer Method.
 - Handles Directory instructions outside of Trimmer Method.

**Parameters:*
 - instruct (InstructionData): Data describing a trim operation step.
 - trim_method (Callable): A path_operation method, applied to File Instructions.
 - move_files (bool): Whether the operation moves files, rather than copies.

**Returns:**
 bool - True if operation succeeds. False if OSError occurs, or trimmer method canceled file operation.
    """
    try:
        if instruct.is_dir: # handle cleaning up empty directories.
            return path_operations.remove_empty_dir(instruct.path)
        elif instruct.data_path is None:
            if move_files:
                if exact:
                    instruct.path.unlink(missing_ok=True)
                else:
                    return False # Nothing can be done with this instruction in this mode
        else:
            return trim_method(instruct)
    except OSError:
        return False
    return True


def _get_path_method(
    control_mode: ControlMode,
    move_files: bool,
) -> Callable[[Path, Path], bool]:
    """ The Path Operation Method that corresponds with given ControlMode, and does either a move or a copy during execution.
 - The first Path parameter in the Operation Method is the TargetFile, the one that will be written to (if ControlMode permits).
 - The second Path parameter is the SourceFile, the one that is moved or copied from.

**Parameters:**
 - control_mode (ControlMode): The set of Control options given to the program during initialization.
 - move_files (bool): Whether to configure the operation to move files, instead of copy.

**Returns:**
 Callable[[Path, Path], bool] - A Method that applies consistent file operations on given Path parameters.
    """
    if isinstance(control_mode, WriteControlModes):
        return path_operations.get_write_operation(move_files, control_mode.overwrite, control_mode.exact_build)
    elif isinstance(control_mode, TextMergeControlModes):
        return path_operations.get_text_merge_method(move_files, control_mode.prepend_merge)
    else:
        raise TypeError
