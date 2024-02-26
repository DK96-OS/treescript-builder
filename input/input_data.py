from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InputData:
    """A Data Class Containing Program Input.

    Fields:
    - tree_input (str): The Tree Input to the FTB operation.
    - data_dir (str, optional): An Optional Path to the Data Directory.
    - is_reversed (bool): Whether this FTB operation is reversed.
    """

    tree_input: str
    data_dir: Optional[Path]
    is_reversed: bool
