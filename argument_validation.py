import argparse
from input_data import InputData
from typing import Optional
from pathlib import Path


class ArgumentValidation:
    """Process and Validate the Arguments."""

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            description="File Tree Builder"
        )
        self._define_arguments()
        self.parsed_args = None
        self.input_data = None
    
    def _define_arguments(self):
        """Defines the command line arguments and their properties."""
        # Required argument
        self._parser.add_argument(
            'tree_file',
            type=str,
            help='The File containing the Tree Node Structure'
        )
        # Optional argument
        self._parser.add_argument(
            '--data_dir',
            default=None,
            help='The Data Directory'
        )

    def parse_args(self, args: Optional[list[str]] = None) -> bool:
        """Parses command line arguments.

        Parameters:
        - args: A list of argument strings.

        Returns:
        Boolean : Whether the arguments were parsed and validated.
        """
        if args is None or len(args) == 0:
            self.parsed_args = None
            return False
        try:
            self.parsed_args = self._parser.parse_args(args)
            self._validate_arguments()
        except:
            self.parsed_args = None
            return False
        return True

    def _validate_arguments(self):
        """Validates the parsed command line arguments."""
        if self.parsed_args is None:
            raise ValueError("Arguments are Missing or Invalid.")
        # Validate Tree
        tree_file = self.parsed_args.tree_file
        if tree_file is None or not isinstance(tree_file, str):
            raise ValueError("The Tree File argument cannot be empty.")
        elif len(tree_file) < 1:
            raise ValueError("The Tree File name cannot be empty.")
        tree_file_path = Path(tree_file)
        if not tree_file_path.exists():
            raise IOError("The Tree Input File does not Exist.")
        # Validate Data Directory, if it exists
        data_dir = self.parsed_args.data_dir
        if data_dir is None:
            data_path = None
            return
        if not isinstance(data_dir, str):
            raise ValueError("The Data Directory must be a String")
        data_path = Path(data_dir)
        if not data_path.exists():
            raise IOError("This Data Directory does not exist!")
        # Valid Input
        self.input_data = InputData(
            tree_file_path,
            data_path
        )
    
    def get_input(self) -> InputData:
        """Obtain the Input Data object from the most recently parsed arguments.

        Returns:
        InputData | None : Container for Valid Input Data.
        """
        if self.input_data is None:
            return None
        return self.input_data
