""" Valid Input Data Class.
 Author: DK96-OS 2024 - 2025
"""
from dataclasses import dataclass
from pathlib import Path

from treescript_builder.data.control_modes import WriteControlModes, TextMergeControlModes, ControlMode


@dataclass(frozen=True)
class InputData:
    """ A Data Class Containing Program Input.

**Fields:**
 - tree_input (str): The Tree Input to the operation.
 - data_dir (Path?): An Optional Path to the DataDirectory.
 - trim_tree (bool): Whether the operation is trim, instead of build.
 - move_files (bool): Whether to Move files instead of copying.
 - control_mode (ControlModeEnum): The control behaviour around validation, overwrite prevention, and error handling.
 - verbosity_level (int): The amount of information to print out. Zero prints nothing.
    """
    tree_input: str
    data_dir: Path | None
    trim_tree: bool
    move_files: bool
    control_mode: ControlMode
    verbosity_level: int

    def __post_init__(self):
        if not (isinstance(self.control_mode, WriteControlModes) or
                isinstance(self.control_mode, TextMergeControlModes)):
            raise TypeError
