"""The Arguments Received from the Command Line Input.
"""
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """The syntactically valid arguments recevied by the Program.
    """

    input_file_path_str: str
    data_dir_path_str: Optional[str]
    is_reversed: bool
