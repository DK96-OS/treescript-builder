"""Instruction DataClass.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class InstructionData:
    """
    An Instruction to the procedural algorithm.

    Fields:
    - depth (int): The depth in the tree of this operation.
    - is_dir (bool): Whether the operation acts on a directory.
    - name (str): The Name of the Tree Node.
    - data_label (str): The Data Label.
    """
    
    depth: int
    is_dir: bool
    name: str
    data_label: str
