"""Data Directory Management.
"""
from pathlib import Path
from sys import exit
from typing import Optional

from data.data_files import is_valid_data_label


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
        if not is_valid_data_label(data_label):
            return None
        #
        data_path = self._data_dir.resolve(data_label)
        if not data_path.exists():
            return None
        #
        return data_path
