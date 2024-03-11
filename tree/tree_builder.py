"""Tree Building Operations
"""
from pathlib import Path
from typing import Generator

from input.data_directory import DataDirectory
from tree.instruction_data import InstructionData
from input.tree_data import TreeData
from tree.tree_state import TreeState


def validate_build(
    tree_data: Generator[TreeData, None, None]
    ) -> Generator[InstructionData, None, None]:
    """
    Validate the Build Instructions.

    Parameters:
    - tree_data (Generator[TreeData]): The Generator that provides TreeData.

    Returns:
    Generator[TreeData] - A generator that yields Instructions.
    """
    tree_state = TreeState()
    previous_line_number = 0
    #
    for node in tree_data:
        # First, check the Line Number
        if previous_line_number < node.line_number:
            previous_line_number = node.line_number
        else:
            exit("Invalid Line Number")
        # Next, check the Tree Depth
        depth_change = node.depth - tree_state.get_current_depth()
        #
        if depth_change > 1:
            exit(f"Invalid Depth at Line: {node.line_number}")
        elif depth_change == 1:
            if node.is_dir:
                # Enqueue New Directory
                tree_state.add_to_queue(node.name)
            else:
                # Merge Queue into Stack
                new_dir = tree_state.process_queue()
                if new_dir is not None:
                    # Build Directory
                    yield InstructionData(True, new_dir, None)
                # Build File
                yield InstructionData(False, new_dir + node.name, None)
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
                yield InstructionData(False, tree_state.get_current_path() + node.name, None)
    # Always Finish Build Sequence with ProcessQueue
    remaining_dirs = tree_state.process_queue()
    if remaining_dirs is not None:
        yield InstructionData(True, Path(remaining_dirs), None)


def validate_build_with_data(
    tree_data: Generator[TreeData],
    data_dir: DataDirectory
    ) -> tuple[InstructionData]:
    """
    Validate the Build Instructions with a Data Directory.
    """
    pass


def build(instructions: tuple[InstructionData]):
    """
    Execute the Instructions in build mode.

    Parameters:
    - instructions(tuple[InstructionData]): The Instructions to execute. 
    
    Returns:
    tuple[bool] - The success or failure of each instruction.
    """
    return (_build(i) for i in instructions)


def _build(i: InstructionData) -> bool:
    """
    Execute a single instruction.

    Parameters:
    - instruction(InstructionData): The data required to execute the operation.
    
    Returns:
    bool - Whether the given operation succeeded.
    """
    if i.is_dir:
        return _make_dir_exist(i.path)
    elif i.data_path is None:
        i.path.touch()
        return True
    else:
        return _create_file(i.path, i.data_path)


def _create_file(
    path: Path,
    data: Path
) -> bool:
    """
    Create a File at the given path, with data from the Data Directory.

    Parameters:
    - path (Path): The Path to the File to be created, and written to.
    - data (Path): A Data Directory Path to be copied to the new File.

    Returns:
    bool - Whether the File operation succeeded.
    """
    from input.file_validation import read_file
    data_str = read_file(data)
    if data_str is None or data_str == '':
        path.touch()
    else:
        path.write_text(data_str)
    return True


def _make_dir_exist(
    path: Path
) -> bool:
    """
    Ensure that the Directory at the given Path exists.

    Parameters:
    - path (Path): The Path to the File to be created, and written to.
   
    """
    if path.exists():
        return True
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except:
        return False
