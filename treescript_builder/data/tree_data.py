"""Tree Node DataClass.
 Author: DK96-OS 2024 - 2025
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TreeData:
    """ A DataClass representing a Tree Node.

Fields:
 - line_number (int): The line number of this tree node in the TreeScript file.
 - depth (int): The depth in the tree, from the root. Starts at zero.
 - is_dir (bool): Whether this Node is a directory.
 - name (str): The Name of the Tree Node.
 - data_label (str): The Data Label, may be empty string.
    """

    line_number: int
    depth: int
    is_dir: bool
    name: str
    data_label: str = ''