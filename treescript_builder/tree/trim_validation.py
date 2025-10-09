""" Tree Validation Methods for the Trim Operation.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from typing import Generator

from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.data.tree_data import TreeData
from treescript_builder.data.tree_state import TreeState
from treescript_builder.tree.data_directory import DataDirectory


def validate_trim(
    tree_data: Generator[TreeData, None, None],
    data_dir_path: Path | None = None,
) -> tuple[InstructionData, ...]:
    """ Validate the Trim Instructions.

**Parameters:**
 - tree_data (Generator[TreeData]): The Generator that provides TreeData.
 - data_dir_path (Path?): The optional Path to a Data Directory. Default: None.

**Returns:**
 tuple[InstructionData] - A tuple of InstructionData.
    """
    return tuple(
        _validate_trim_generator(
            tree_data=tree_data,
            data_dir=DataDirectory(data_dir_path) if data_dir_path is not None else None,
        )
    )


def _validate_trim_generator(
    tree_data: Generator[TreeData, None, None],
    data_dir: DataDirectory | None,
) -> Generator[InstructionData, None, None]:
    tree_state = TreeState()
    for node in tree_data:
        # Error if no dataDir and Node has no DataLabel. todo: Move this validation earlier in the program. (line_reader, maybe)
        if data_dir is None and node.data_label != '':
            exit(f"No DataDirectory provided, but DataLabel found on Line: {node.line_number}")
        # Calculate Tree Depth Change
        if tree_state.validate_tree_data(node) != 1: # Pop Stack to required Depth
            for trim_dir_path in tree_state.process_stack(node.depth):
                yield InstructionData(True, trim_dir_path)
        if node.is_dir:
            tree_state.add_to_stack(node.name)
        else:
            yield InstructionData(
                False,
                tree_state.get_current_path() / node.name,
                data_dir.validate_trim(node) if data_dir is not None else None
            )
    # Finish Trim Sequence with Pop Stack
    for trim_dir_path in tree_state.process_stack(0):
        yield InstructionData(True, trim_dir_path)
