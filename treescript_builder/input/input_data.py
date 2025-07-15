""" Valid Input Data Class.
 Author: DK96-OS 2024 - 2025
"""
from dataclasses import dataclass
from pathlib import Path

from treescript_builder.data.file_mode_enum import FileModeEnum


@dataclass(frozen=True)
class InputData:
    """A Data Class Containing Program Input.

**Fields:**
 - tree_input (str): The Tree Input to the FTB operation.
 - data_dir (Path?): An Optional Path to the Data Directory. Default: None
 - is_reversed (bool): Whether this FTB operation is reversed. Default: False
 - mode (FileModeEnum): The Mode of File Operation. Default: FileModeEnum.APPEND. Other options: PREPEND, OVERWRITE.
    """
    tree_input: str
    data_dir: Path | None = None
    is_reversed: bool = False
    mode: FileModeEnum = FileModeEnum.APPEND
