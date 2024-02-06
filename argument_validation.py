import argparse
from input_line_reader import process_many_lines


class ArgumentValidation:
    """Process and Validate the Arguments.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="File Tree Builder")
        self._define_arguments()
        self.args = self.parser.parse_args()
        self._validate_arguments()
    
    def _define_arguments(self):
        """Defines the command line arguments and their properties.
        """
        # Required argument
        self.parser.add_argument('tree_input', type=str, help='The File containing the Tree Node Structure')
        # Optional argument
        self.parser.add_argument('data_directory', type=str, metavar='OPTION', help='The Data Directory')
        # Potential Future Flags
        #self.parser.add_argument('-r', '--remove', action='store_true', help='')

    def _validate_arguments(self):
        """Validates the parsed command line arguments.
        """
        if not self.args.tree_input:
            self.parser.error("The Tree Input argument cannot be empty.")
    
    def get_tree_input(self):
        """Obtains the Input Data from the File.
        """
        file_path = self.args.input_tree
        with open(file_path, 'r') as file:
            input_tree = file.read()
        # Check the Input
        if input_tree is None or len(input_tree) < 1:
            raise ValueError("Tree Input not found, or empty.")
        # Process the Input Tree
        return process_many_lines(input_tree)

    def get_data_dir(self):
        """Obtain the Data Directory.
        """
        return self.args.data_directory
