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
    main()
