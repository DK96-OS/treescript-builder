"""Data File Methods.
"""
from typing import Optional


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
