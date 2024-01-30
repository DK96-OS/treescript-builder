""" The Default Input Reader.
    Processes a single line at a time, and determines it's key properties.
    The Depth is the Integer number of directories between the current line and the root.
    The Directory Boolean indicates whether the line represents a Directory.
    The Name String is the name of the line.
"""

# The acceptable characters for space
SPACE_CHARS = (' ', ' ', ' ', ' ')


def calculate_depth(line: str) -> int:
    """
    Calculates the depth of a line in the tree structure.

    Parameters:
    - line (str): A line from the tree command output.

    Returns:
    int: The depth of the line in the tree structure.
    """
    depth = 0
    space_count = 0
    #
    for char in line:
        if char in SPACE_CHARS:
            space_count += 1
            if space_count > 1:
                space_count = 0
                depth += 1
        else:
            break
    return depth


def create_depth(depth: int, space_char: int = 0) -> str:
    """
		Convert each of the Space Chars into a string of them equivalent to the given depth.

		Parameters:
		- depth (int): The amount of depth in the Tree Node Structure.
		- space_char (int): The specific whitespace character to use. Default is the first.

		Returns:
		str: The Strings for each Space Char, of a given depth length.
		"""
    char = SPACE_CHARS[0]
    if 0 < space_char < len(SPACE_CHARS):
        char = SPACE_CHARS[space_char]
    # Default
    return char * depth * 2


def process_line(line: str) -> tuple[int, bool, str, str]:
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
    for space_char in SPACE_CHARS:
        if space_char in args:
            args = args.split(space_char)
            break
    if args is not list:
        args = [args]
    if len(args) == 1:
        # Do nothing different, there is no second argument
        name = args[0]
        data_file = ""
    elif (len(args) >= 2):
        name = args[0]
        data_file = args[1]
    else:
        name = "Default"
        data_file = ""
    # Check if the line represents a directory.
    is_dir = name.endswith('/') or name.startswith('/')  
    is_dir = is_dir or name.endswith('\\') or name.startswith('\\')
    if is_dir:
        # Extract the name, removing '/' or '\' if present.
        name = name.strip('/\\')
    # Produce Tuple
    return calculate_depth(line), is_dir, name, data_file
