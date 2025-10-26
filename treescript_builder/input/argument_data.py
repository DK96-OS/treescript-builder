""" The Arguments Received from the Command Line Input.
 - This DataClass is created after the argument syntax is validated.
 - Syntax Validation:
    - Argparse accepts the given CLI arguments.
    - The Input File is Present and non-blank.
    - When Data Directory is present, it is non-blank.
 Author: DK96-OS 2024 - 2025
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """ The syntactically valid arguments received by the Program.
 - All default values for ArgumentData fields are either False, or 0.
 - This is for predictability and testability, and does not reflect the true defaults of the program.
 - The positional str arguments have no defaults.

**Fields:**
 - input_file_path_str (str): The Name of the File containing the Tree Structure.
 - data_dir_path_str (str?): The Directory Name containing Files used in File Tree Operation.
 - trim_tree (bool): The Trim operation is the inverse of the Build operation.
 - move_files (bool): Option that moves files instead of copying.
 - text_append (bool): Mode of appending Text data at the start of existing files. Creates the Target file if necessary.
 - text_prepend (bool): Mode of prepending Text data at the start of existing files. Creates the Target file if necessary.
 - control_continue (bool): ControlMode that continues the build after errors, while preventing overwriting non-empty files.
 - control_overwrite (bool): ControlMode that overwrites existing files when combined with Replace TextMode.
 - control_validate (bool): ControlMode that increases the scope of the validation phase. An extra layer on top of Cancel ControlMode.
 - control_exact_build (bool): ControlMode that increases build precision, by removing a default file content safety check.
 - verbosity (int): The amount of info to print to output. L0: No Output. L1: Failed FileTree Operations. L2: All FileTree Operations.
    """
    input_file_path_str: str
    data_dir_path_str: str | None
    trim_tree: bool = False
    move_files: bool = False
    # Text Mode Options
    text_append: bool = False
    text_prepend: bool = False
    # Control Mode Options
    control_continue: bool = False
    control_overwrite: bool = False
    control_validate: bool = False
    control_exact_build: bool = False
    verbosity: int = 0
