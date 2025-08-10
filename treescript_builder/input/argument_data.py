""" The Arguments Received from the Command Line Input.
 - This DataClass is created after the argument syntax is validated.
 - Syntax Validation:
    - The Input File is Present and non-blank.
    - When Data Directory is present, it is non-blank.
 Author: DK96-OS 2024 - 2025
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """ The syntactically valid arguments received by the Program.
- The Default Mode Appends data to the end of existing files.

**Fields:**
 - input_file_path_str (str): The Name of the File containing the Tree Structure.
 - data_dir_path_str (str?): The Directory Name containing Files Used in File Tree Operation. Default: None.
 - is_reversed (bool): The reversed FileTree Build operation is called the Trim operation. Default: False.
 - verbosity (int): The amount of info to print to output. L0: No Output. L1: Failed FileTree Operations. L2: All FileTree Operations. Default: 0.
 - cancel (bool): Optional Mode that cancels any file operation that may overwrite existing file data. Default: False.
 - move (bool): Optional Mode that moves files instead of copying. Default: False.
 - overwrite (bool): Optional Mode of overwriting data in existing files. Default: False.
 - prepend (bool): Optional Mode of prepending data at the start of existing files. Default: False.
    """
    input_file_path_str: str
    data_dir_path_str: str | None = None
    is_reversed: bool = False
    verbosity: int = 0
    # File Mode Options:
    cancel: bool = False
    move: bool = False
    overwrite: bool = False
    prepend: bool = False
