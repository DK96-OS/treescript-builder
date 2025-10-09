""" Tree Validation Methods for the Build Operation.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from typing import Generator

from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.data.tree_data import TreeData
from treescript_builder.data.tree_state import TreeState
from treescript_builder.tree.data_directory import DataDirectory


def validate_build(
    tree_data: Generator[TreeData, None, None],
    data_dir_path: Path | None = None,
) -> tuple[InstructionData, ...]:
    """ Validate the Build Instructions.

**Parameters:**
 - tree_data (Generator[TreeData]): The Generator that provides TreeData.
 - data_dir_path (Path?): The optional Data Directory Path. Default: None.

**Returns:**
 tuple[InstructionData] - A generator that yields Instructions.
    """
    return tuple(
        _validate_build_generator(
            tree_data=tree_data,
            data_dir=DataDirectory(data_dir_path) if data_dir_path is None else None
        )
    )


def _validate_build_generator(
    tree_data: Generator[TreeData, None, None],
    data_dir: DataDirectory | None,
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Error if no dataDir and Node has no DataLabel. todo: Move this validation earlier in the program. (line_reader, maybe)
        if data_dir is None and node.data_label != '':
            exit(f"No DataDirectory provided, but DataLabel found on Line: {node.line_number}")
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) == 0:
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                # Merge Queue into Stack
                if (new_dir := tree_state.process_queue()) is not None:
                    yield InstructionData(True, new_dir)
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    data_dir.validate_build(node) if data_dir is not None else None,
                )
        else:
            # Merge Queue into Stack
            if (new_dir := tree_state.process_queue()) is not None:
                yield InstructionData(True, new_dir)
            # Pop Stack to required Depth
            if not tree_state.reduce_depth(node.depth):
                exit(f"Invalid Tree Depth in Line: {node.line_number} : {node.name}")
            if node.is_dir:
                tree_state.add_to_queue(node.name)
            else:
                yield InstructionData(
                    False,
                    tree_state.get_current_path() / node.name,
                    data_dir.validate_build(node) if data_dir is not None else None,
                )
    # Always Finish Build Sequence with ProcessQueue
    if (new_dir := tree_state.process_queue()) is not None:
        yield InstructionData(True, new_dir)
