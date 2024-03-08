"""Tree Validation Methods.
"""
from itertools import takewhile
from typing import Generator

from input.data_directory import DataDirectory
from input.tree_data import TreeData
from tree.instruction_data import InstructionData
from tree.path_stack import PathStack


def validate_tree(
    tree_data_generator: Generator[TreeData, None, None]
    ) -> tuple[InstructionData, ...]:
    """
    Process Tree Data into executable instructions.
        Assume there is no data directory.
    """
    inst = []
    path_stack = PathStack()
    return (
        
    )


def validate_with_data_dir(
    tree_data_generator: Generator[TreeData, None, None],
    data_dir: DataDirectory
    ) -> tuple[InstructionData, ...]:
    """
    Validate Tree alongside the Data directory.
    """
    inst = []
    path_stack = PathStack()
    return (

    )
