"""The Arguments Received from the Command Line Input.

This DataClass is created after the argument syntax is validated.

Syntax Validation:
- The Input File is Present and non-blank.
- When Data Directory is present, it is non-blank.
"""
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """
    The syntactically valid arguments recevied by the Program.

    Fields:
    - input_file_path_str (str): The Path String to the (Tree) Input File.
    - data_dir_path_str (str, optional): The Path String to the Data Directory.
    - is_reversed (bool): Whether the Tree Operation is Reversed.
    """

    input_file_path_str: str
    data_dir_path_str: Optional[str]
    is_reversed: bool
