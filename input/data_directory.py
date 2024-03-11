"""Data Directory Management.
"""
from pathlib import Path
from sys import exit
from typing import Optional

from input.string_validation import validate_data_label
from input.tree_data import TreeData


class DataDirectory:
    """
    Manages Access to the Data Directory.
        Search for a Data Label, and obtain the Path to the Data File.
    """

    def __init__(self, data_dir: Path):
        if not isinstance(data_dir, Path):
            exit('The Data Directory must be a Path.')
        if not data_dir.exists():
            exit('The given Data Directory does not Exist.')
        self._data_dir = data_dir

    def search_label(self, data_label: str) -> Optional[Path]:
        """
        Search for a Data Label in this Data Directory.

        Parameters:
        - data_label (str): The Data Label to search for.

        Returns:
        Path (optional) - The Path to the Data File, or None.
        """
        if not validate_data_label(data_label):
            return None
        # Find the Data Label File
        data_files = self._data_dir.glob(data_label)
        try:
            return next(data_files)
        except StopIteration as s:
            return None

    def process_tree_data(self, node: TreeData) -> Optional[Path]:
        """
        Process the Data Label 
        """
        if node.data_label == '':
            return None
        data_path = self.search_label(node.data_label)
        if data_path is None:
            exit(f'Data Label on Line {node.line_number} not found in Data Directory: {node.data_label}')
        return data_path

    def check_trim(self, node: TreeData) -> Path:
        """
        Determine if the File already exists in the Data Directory.
        """
        if node.data_label == '':
            exit('Data Label !!!!!!!!!!')
        #
        data_path = self.search_label(node.data_label)
        if data_path is not None:
            exit('Data already Exists')
        #
        if not validate_data_label(node.data_label):
            exit('Data Label is invalid')
        #
        return self._data_dir / node.data_label
