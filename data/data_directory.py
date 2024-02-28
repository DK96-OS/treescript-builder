"""Data Directory Management.
"""
from typing import Optional
from pathlib import Path


class DataDirectory:
    """Manages Access to the Data Directory.
    """

    def __init__(self, data_dir: Path, type_splitting: bool = False):
        """
        """
        self._data_dir = data_dir
        self.type_splitting = type_splitting

    def search_label(self, file_name: str, data_label: str) -> Optional[Path]:
        """
        """
        # todo:
        self._data_dir.resolve(file_name)
        #
        pass

    def search_name(self, file_name: str) -> Optional[Path]:
        """
        """
        # todo:
        pass
