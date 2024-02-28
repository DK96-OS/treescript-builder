"""Line Reader.

The Default Input Reader.
    Processes a single line at a time, and determines its key properties.
    The Depth is the Integer number of directories between the current line and the root.
    The Directory Boolean indicates whether the line represents a Directory.
    The Name String is the name of the line.
"""
from data.instruction_data import InstructionData


SPACE_CHARS = (' ', ' ', ' ', ' ')


def process_line(line: str) -> InstructionData:
    """
    Processes a single line of the input tree structure.
    Returns a tuple indicating the depth, type (file or directory), name of file or dir, and file data if available.

    Parameters:
    - line (str): A line from the input tree structure.

    Returns:
    tuple: (int, bool, str, str) where int is the depth, bool is true when is Directory, and str is name, followed by str data.
    """    
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
        data_file = ""
    elif isinstance(args, list):
        if len(args) == 1:
            # Do nothing different, there is no second argument
            name = args[0]
            data_file = ""
        elif len(args) >= 2:
            name = args[0]
            data_file = args[1]
    else:
        print("Unknown Type: "+ str(type(args)))
        name = "Default"
        data_file = ""
    # Check if the line represents a directory.
    is_dir = name.endswith('/') or name.startswith('/')  
    is_dir = is_dir or name.endswith('\\') or name.startswith('\\')
    if is_dir:
        # Extract the name, removing '/' or '\' if present.
        name = name.strip('/\\')
    return InstructionData(
        _calculate_depth(line), is_dir, name, data_file
    )


def _calculate_depth(line: str) -> int:
    """
    Calculates the depth of a line in the tree structure.

    Parameters:
    - line (str): A line from the tree command output.

    Returns:
    int: The depth of the line in the tree structure.
    """
    from itertools import takewhile
    space_count = len(list(
        takewhile(lambda c: c in SPACE_CHARS, line)
    ))
    depth = space_count >> 1
    if depth << 1 == space_count:
        return depth
    raise ValueError("Invalid Space Count in Line: " + line)
