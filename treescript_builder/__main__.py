#!/usr/bin/python


def main():
    # Author: DK96-OS 2024 - 2025
    from sys import argv
    # Process Arguments with Input Package
    from treescript_builder.input import validate_input_arguments
    input_data = validate_input_arguments(argv[1:])
    # Validate & Build Tree with Operations Package
    from treescript_builder.operations import tree_operations
    if 0 < len(result := tree_operations(input_data)):
        print(result) # Non-empty result str.


if __name__ == "__main__":
    from sys import path
    from pathlib import Path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    path.append(str(current_directory)) # Add the directory to sys.path
    main()
