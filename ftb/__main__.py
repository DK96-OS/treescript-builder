"""File Tree Builder Main Startup Script.
"""
import sys


def main():
    """
    Validates Arguments, then runs File Tree Builder.
    """
    from input import validate_input_arguments
    from tree import build_tree
    # Validate and Process Input
    build_tree(validate_input_arguments(sys.argv[1:]))
    

if __name__ == "__main__":
    from pathlib import Path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    # Add the directory to sys.path
    sys.path.append(str(current_directory))
    #
    main()
