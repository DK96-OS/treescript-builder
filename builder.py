#!/usr/bin/python
""" File Tree Builder
    Builds a File Tree from a given input.
"""
# Default Input Reader
from input_line_reader import process_line


def join_path_stack(stack: list[str]) -> str:
    """
    Combines all elements in the path Stack to form the parent directory.

    Parameters:
    - stack (list): The stack of directories leading to the parent directory.

    Returns:
    String path representing the parent directory.
    Does not start with /, but ends with one.
    """
    # Add each element in the path
    return "/".join(stack) + "/"


def build_tree(input_tree: str, data_directory: str = '.', ):
    """
    Builds the directory tree from the input structure.

    Parameters:
    - input_tree (str): The Tree Node Structure Input as a string.
    - root_path (str, optional): The path at the base of the Tree. Defaults to '.'.

    Returns:
    None
    """
    import os
    #
    path_stack = ['.']
    # Divide the Input Data into Lines
    lines = input_tree.strip().split('\n')
    # Process one line at a time
    for line in lines:
        depth, is_dir, name, data = process_line(line)
        # Adjust path stack to current depth.
        while len(path_stack) > depth + 1:
            path_stack.pop()  # Remove the last element to match the current depth.
        # Form the full path for the file or directory.
        full_path = join_path_stack(path_stack) + name
        # Create the actual tree node in the file system
        if is_dir:
            os.makedirs(full_path, exist_ok=True)
            # Add the new directory to the path stack.
            path_stack.append(name)
        else:
            with open(full_path, 'w') as f:
                f.write(data)
                # todo: implement File Data Directory


def check_empty_dir(dir_path: str) -> bool:
    """

    """
    # todo: Check if this directory is empty
    # todo: Check the length of the contents of the directory
    return False


def trim_tree():
    """
    Removes specific Files and Empty Directories from the File System.

    Parameters:
    - input_tree (str): The Tree Node Structure Input as a string.
    - root_path (str, optional): The path at the base of the Tree. Defaults to '.'.

    Returns:
    None
    """
    import os
    #
    path_stack = [root_path]
    # Divide the Input Data into Lines
    lines = input_tree.strip().split('\n')
    # 
    for line in lines:
        # Deconstruct the Line Data
        depth, is_dir, name, _ = process_line(line)
        # Adjust the Path Stack to the Line Depth.
        while len(path_stack) > depth + 1:
            # Pop a Directory, Check if it is empty
            closed_dir = path_stack.pop()
            
            if check_empty_dir(join_path_stack(path_stack) + closed_dir):
                # todo: Remove the directory from the file system
                pass
        
        # Form the full path for the file or directory.
        full_path = join_path_stack(path_stack) + name
        # Create the actual tree node in the file system
        if is_dir:
            # Add the directory to the path stack.
            path_stack.append(name)
        else:
            with open(full_path, 'w') as f:
                pass # todo: Delete File

    # Check the Path Stack for Remaining Directories
    while len(path_stack) > 1:
        # Check if the Directory is empty
        # If it is remove it
        # If not break the loop and exit
        break


def main():
    """
    The main function that initiates the tree building process.

    It reads the file path from the command line argument, reads the tree structure from the file,
    and calls build_tree to construct the directory structure.

    Returns:
    None
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage: python builder.py <path_to_tree_structure_file>")
        sys.exit(1)
    # Required argument
    file_path = sys.argv[1]
    # Optional argument
    if (len(sys.argv) >= 3):
        # Next Argument is the Data Directory
        data_directory = sys.argv[2]
    else:
        data_directory = ""
    # Read the Tree Node Structure Input from the File
    with open(file_path, 'r') as file:
        input_tree = file.read()
    #
    build_tree(input_tree, data_directory)


if __name__ == "__main__":
    main()
