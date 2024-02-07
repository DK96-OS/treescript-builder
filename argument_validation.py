import argparse
from input_data import InputData
from typing import Optional


class ArgumentValidation:
    """Process and Validate the Arguments."""

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            description="File Tree Builder"
        )
        self._define_arguments()
        self.parsed_args = None
    
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
        elif not self.parsed_args.tree_file:
            raise ValueError("The Tree File argument cannot be empty.")
    
    def get_input(self) -> InputData:
        """Obtain the Input Data object from the most recently parsed arguments.

        Returns:
        InputData | None : Container for Valid Input Data.
        """
        if self.parsed_args is None:
            return None
        return InputData(
            self.parsed_args.tree_file,
            self.parsed_args.data_dir
        )
