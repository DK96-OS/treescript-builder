"""Tree Validation Methods.
"""
from itertools import takewhile
from pathlib import Path
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
    tree_Data = _validate_tree_structure(tree_data_generator)
    #
    inst = []
    path_stack = PathStack()
    # More state
    last_tree_node = None
    #
    for t_data in tree_data_generator:
        # Check Is Directory
        if t_data.is_dir:
            #
            success = path_stack.reduce_depth(t_data.depth)
            if not success:
                exit(f"Inconsistent Tree Depth at Line: {t_data.line_number}")
            #
            path_stack.push(t_data.name)
            # todo: Optimize 
            inst.append(InstructionData(True, Path(path_stack.join_stack()), None))
        else:
            file_path = path_stack.create_path(t_data.name)
            inst.append(InstructionData(False, file_path, None))
        #
    # todo: Empty Path Stack
    return tuple(inst)


def validate_with_data_dir(
    tree_data_generator: Generator[TreeData, None, None],
    data_dir: DataDirectory
    ) -> tuple[InstructionData, ...]:
    """
    Validate Tree alongside the Data directory.
    """
    inst = []
    path_stack = PathStack()
    return ()


def _validate_tree_structure(tree_generator: Generator[TreeData, None, None]) -> tuple[TreeData]:
    data = []
    for t in tree_generator:
        data.append(t)
    #
    pass
    return tuple(data)
