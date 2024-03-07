"""Data Directory Management.
"""
from pathlib import Path
from sys import exit
from typing import Optional

from input.string_validation import validate_data_label


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

    def send_label(self, data_label: str, data: str) -> bool:
        """
        Send Labelled Data to the Data Directory.

        Parameters:
        - data_label (str): The Label to store the data in.
        - data (str): The Data to Store in the Data Directory.

        Returns:
        bool - True if the Label is valid, and the Data Directory accepted the data.
        """
        if not validate_data_label(data_label):
            return False
        #
        data_path = self._data_dir / data_label
        # If the File already exists, cancel
        if data_path.exists():
            return False
        try:
            data_path.write_text(data)
            return True
        except IOError as e:
            return False
