"""Tree Validation Methods.
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
    if data_dir is None:
        return tuple(_ for _ in _validate_build_generator(tree_data))
    else:
        return tuple(_ for _ in _validate_build_generator_data(tree_data, data_dir))


def validate_trim(
    tree_data: Generator[TreeData, None, None],
    data_dir: Optional[DataDirectory]
) -> tuple[InstructionData, ...]:
    """    
    Validate the Trim Instructions.

    Parameters:
    - tree_data (Generator[TreeData]): The Generator that provides TreeData.
    - data_dir (DataDirectory, optional): The optional Data Directory.

    Returns:
    tuple[InstructionData] - A generator that yields Instructions.
    """
    if data_dir is None:
        return tuple(_ for _ in _validate_trim_generator(tree_data))
    else:
        return tuple(_ for _ in _validate_trim_generator_data(tree_data, data_dir))


def _validate_build_generator(
    tree_data: Generator[TreeData, None, None]
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Error if any Nodes have Data Labels
        if node.data_label != '':
            exit(f"Found Data Label on Line {node.line_number} with no Data Directory: {node.data_label}")
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) == 1:
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                # Merge Queue into Stack
                new_dir = tree_state.process_queue()
                if new_dir is not None:
                    yield InstructionData(True, new_dir, None)
                yield InstructionData(False, new_dir / node.name, None)
        else:
            # Merge Queue into Stack
            new_dir = tree_state.process_queue()
            if new_dir is not None:
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
    remaining_dirs = tree_state.process_queue()
    if remaining_dirs is not None:
        yield InstructionData(True, remaining_dirs, None)


def _validate_build_generator_data(
    tree_data: Generator[TreeData, None, None],
    data_dir: DataDirectory
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) == 1:
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                # Build Queued Directories
                new_dir = tree_state.process_queue()
                if new_dir is not None:
                    yield InstructionData(True, new_dir, None)
                # Build File
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    data_dir.process_tree_data(node)
                )
        else:
            # Merge Queue into Stack
            new_dir = tree_state.process_queue()
            if new_dir is not None:
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
                    data_dir.process_tree_data(node)
                )
    # Always Finish Build Sequence with ProcessQueue
    remaining_dirs = tree_state.process_queue()
    if remaining_dirs is not None:
        yield InstructionData(True, remaining_dirs, None)


def _validate_trim_generator(
    tree_data: Generator[TreeData, None, None]
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) == 1:
            if node.is_dir:
                tree_state.add_to_stack(node.name)
            else:
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    None
                )
        else:
            # Pop Stack to required Depth
            for i in tree_state.process_stack(node.depth):
                yield InstructionData(True, i, None)
            # Dir or File
            if node.is_dir:
                tree_state.add_to_stack(node.name)
            else:
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    None
                )
    # Finish Trim Sequence with Pop Stack
    for i in tree_state.process_stack(0):
        yield InstructionData(True, i, None)


def _validate_trim_generator_data(
    tree_data: Generator[TreeData, None, None],
    data_dir: DataDirectory
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) == 1:
            if node.is_dir:
                tree_state.add_to_stack(node.name)
            else:
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    data_dir.check_trim(node)
                )
        else:
            # Pop Stack to required Depth
            for i in tree_state.process_stack(node.depth):
                yield InstructionData(True, i, None)
            # Dir or File
            if node.is_dir:
                tree_state.add_to_stack(node.name)
            else:
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    data_dir.check_trim(node)
                )
    # Finish Trim Sequence with Pop Stack
    for i in tree_state.process_stack(0):
        yield InstructionData(True, i, None)
