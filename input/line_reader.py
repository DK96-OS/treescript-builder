"""Line Reader.

The Default Input Reader.
    Processes a single line at a time, and determines its key properties.
    The Depth is the Integer number of directories between the current line and the root.
    The Directory Boolean indicates whether the line represents a Directory.
    The Name String is the name of the line.
"""
from itertools import groupby
from sys import exit
from typing import Generator

from input.tree_data import TreeData


SPACE_CHARS = (' ', ' ', ' ', ' ')


def read_input_tree(input_tree_data: str) -> Generator[TreeData, None, None]:
    """
    Generate structured Tree Data from the Input Data String.

    Parameters:
    - input_data (InputData): The Input.

    Returns:
    Generator[TreeData] - Produces TreeData from the Input Data.

    Raises:
    SystemExit - When any Line cannot be read successfully.
    """
    line_number = 1
    for is_newline, group in groupby(input_tree_data, lambda x: x == "\n"):
        if not is_newline:
            line = ''.join(group)
            if line.lstrip().startswith('#'):
                continue
            yield _process_line(line_number, line)
        else:
            line_number += 1


def read_input_tree_to_tuple(input_tree_data: str) -> tuple[TreeData, ...]:
    """
    Process Multiple Lines from the Tree Node Structure Input.

    Parameters:
    - input_data (InputData): The Input containing multiple lines of tree node data.

    Returns:
    tuple[InstructionData] - The Tuple of Instruction Data, read from the Input String.

    Raises:
    SystemExit - When any Line cannot be read successfully.
    """
    all_lines = enumerate(input_tree_data.split("\n"), start=1)
    return (
        _process_line(n, line) for n, line in filter(
            all_lines, lambda _, x: not x.lstrip().startswith('#')
        )
    )


def _process_line(line_number: int, line: str) -> TreeData:
    """
    Processes a single line of the input tree structure.
    Returns a tuple indicating the depth, type (file or directory), name of file or dir, and file data if available.

    Parameters:
    - line (str): A line from the input tree structure.

    Returns:
    tuple: (int, bool, str, str) where int is the depth, bool is true when is Directory, and str is name, followed by str data.

    Raises:
    SystemExit - When Line cannot be read successfully.
    """
    # Calculate the Depth
    depth = _calculate_depth(line)
    if depth < 0:
        exit(f"Invalid Space Count in Line: {line_number}")
    # Remove Space
    args = line.strip()
    # Try to split line into multiple arguments
    for space_char in SPACE_CHARS:
        if space_char in args:
            args = args.split(space_char)
            break
    # Check whether line was split or not
    if isinstance(args, str):
        name = args
        data_label = ""
    elif isinstance(args, list) and len(args) >= 2:
        name = args[0]
        data_label = args[1]
    else:
        exit(f"Invalid Line: {line_number}")
    # Check if the line represents a directory.
    is_dir = name.endswith('/') or name.startswith('/')  
    is_dir = is_dir or name.endswith('\\') or name.startswith('\\')
    if is_dir:
        # Extract the name, removing '/' or '\' if present.
        name = name.strip('/\\')
    return TreeData(
        line_number,
        depth,
        is_dir,
        name,
        data_label
    )


def _calculate_depth(line: str) -> int:
    """
    Calculates the depth of a line in the tree structure.

    Parameters:
    - line (str): A line from the tree command output.

    Returns:
    int: The depth of the line in the tree structure, or -1 if space count is invalid.
    """
    from itertools import takewhile
    space_count = len(list(
        takewhile(lambda c: c in SPACE_CHARS, line)
    ))
    depth = space_count >> 1
    if depth << 1 == space_count:
        return depth
    # Invalid Space Count: Negative 1
    return -1
