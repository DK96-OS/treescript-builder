"""Tree Validation Methods for the Build Operation.
"""
from typing import Generator, Optional

from input.data_directory import DataDirectory
from input.tree_data import TreeData
from tree.instruction_data import InstructionData
from tree.tree_state import TreeState


def validate_build(
    tree_data: Generator[TreeData, None, None],
    data_dir: Optional[DataDirectory]
) -> tuple[InstructionData, ...]:
    """
    Validate the Build Instructions.

    Parameters:
    - tree_data (Generator[TreeData]): The Generator that provides TreeData.
    - data_dir (DataDirectory, optional): The optional Data Directory.

    Returns:
    tuple[InstructionData] - A generator that yields Instructions.
    """
    return tuple(iter(
        _validate_build_generator(tree_data)
        if data_dir is None else
        _validate_build_generator_data(tree_data, data_dir)
    ))


def _validate_build_generator(
    tree_data: Generator[TreeData, None, None]
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Error if any Nodes have Data Labels
        if node.data_label != '':
            exit(f"Found Data Label on Line {node.line_number} with no Data Directory: {node.data_label}")
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) == 0:
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                # Merge Queue into Stack
                if (new_dir := tree_state.process_queue()) is not None:
                    yield InstructionData(True, new_dir, None)
                yield InstructionData(
                    False, tree_state.get_current_path() / node.name, None
                )
        else:
            # Merge Queue into Stack
            if (new_dir := tree_state.process_queue()) is not None:
                yield InstructionData(True, new_dir, None)
            # Pop Stack to required Depth
            if not tree_state.reduce_depth(node.depth):
                exit(f"Invalid Depth at Line: {node.line_number}")
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                yield InstructionData(
                    False, tree_state.get_current_path() / node.name, None
                )
    # Always Finish Build Sequence with ProcessQueue
    if (dir := tree_state.process_queue()) is not None:
        yield InstructionData(True, dir, None)


def _validate_build_generator_data(
    tree_data: Generator[TreeData, None, None],
    data_dir: DataDirectory
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) == 0:
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                # Build Queued Directories
                if (new_dir := tree_state.process_queue()) is not None:
                    yield InstructionData(True, new_dir, None)
                # Build File
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    data_dir.validate_build(node)
                )
        else:
            # Merge Queue into Stack
            if (new_dir := tree_state.process_queue()) is not None:
                yield InstructionData(True, new_dir, None)
            # Pop Stack to required Depth
            if not tree_state.reduce_depth(node.depth):
                exit(f"Invalid Tree Depth on Line {node.line_number} : {node.name}")
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    data_dir.validate_build(node)
                )
    # Always Finish Build Sequence with ProcessQueue
    if (dir := tree_state.process_queue()) is not None:
        yield InstructionData(True, dir, None)
