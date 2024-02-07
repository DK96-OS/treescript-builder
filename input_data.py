from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InputData:
    """The Data provided as input to the Program.

    Parameters:
    - tree_file (str): The path to the file containing the tree input.
    - data_dir (str, optional): The path to the data directory.
    """

    tree_file: str
    data_dir: Optional[str]

    def get_tree_input(self) -> str:
        """Obtain the String contents of the Tree File."""
        tree_path = Path(self.tree_file)
        if not tree_path.exists():
            raise IOError("Tree File does not exist.")
        try:
            return tree_path.read_text()
        except:
            raise IOError("Failed to Read from Tree File.")

    def get_data_dir_path(self) -> Optional[Path]:
        """Obtain a Path to the Data Directory."""
        if self.data_dir is None:
            return None
        return Path(self.data_dir)


def get_input_from_args(arguments: Optional[list[str]]) -> Optional[InputData]:
    """Parse and Validate the Arguments, then return as InputData.

    Returns:
    InputData | None : An InputData object, or None if args are invalid.
    """
    from argument_validation import ArgumentValidation
    args = ArgumentValidation()
    args.parse_args(arguments)
    return args.get_input()
