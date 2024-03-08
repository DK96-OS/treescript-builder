"""Valid Input Data Class.
"""
from typing import Optional, Generator
from dataclasses import dataclass

from input.data_directory import DataDirectory
from input.tree_data import TreeData


@dataclass(frozen=True)
class InputData:
    """A Data Class Containing Program Input.

    Fields:
    - tree_input (str): The Tree Input to the FTB operation.
    - data_dir (str, optional): An Optional Path to the Data Directory.
    - is_reversed (bool): Whether this FTB operation is reversed.
    """

    tree_input: str
    data_dir: Optional[DataDirectory]
    is_reversed: bool

    def get_tree_data(self) -> Generator[TreeData, None, None]:
        """
        Initializes a Generator for processing the Tree Input.
            See line_reader module for more details.

        Returns:
        Generator - Yields one TreeData for each Line of Tree Input.
        """
        from input.line_reader import read_input_tree
        return read_input_tree(self.tree_input)
