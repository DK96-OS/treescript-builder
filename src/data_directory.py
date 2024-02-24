"""Data Directory Management.
"""
from typing import Optional
from pathlib import Path


def get_file_extension(file_name: str) -> Optional[str]:
    """Obtain the last File Extension in a File Name, if it exists.
    """
    try:
        index = file_name[::-1].index('.')
        return file_name[len(file_name) - index:]
    except:
        return None


def is_valid_data_label(data_label: str) -> bool:
    """Determine whether a Data Label is Valid.
    """ 
    return data_label.isalnum()


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
