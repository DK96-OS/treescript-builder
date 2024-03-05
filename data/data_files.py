"""Data File Methods.
"""
from typing import Optional


def get_file_extension(file_name: str) -> Optional[str]:
    """
    Obtain the File Extension, if it exists.
        The Last extension in a multi-part extension is returned.
    
    Parameters:
    - file_name (str): The name of the File.

    Returns:
    str or None - The File Extension, or None.
    """
    try:
        index = file_name[::-1].index('.')
        result = file_name[len(file_name) - index:]
        if len(result) < 1:
            return None
        return result
    except:
        return None


def is_valid_data_label(data_label: str) -> bool:
    """
    Determine whether a Data Label is Valid.

    Parameters:
    - data_label (str): The String to check for validity.

    Returns:
    bool - Whether the String is a valid Data Label.
    """
    if not 0 < len(data_label) < 100:
        return False
    if '/' in data_label or '\\' in data_label:
        return False
    # Remove Dash Characters
    if '-' in data_label:
        data_label = data_label.replace('-', '')
    # Remove Underscore Characters
    if '_' in data_label:
        data_label = data_label.replace('_', '')
    # Remove Dot Characters
    if '.' in data_label:
        data_label = data_label.replace('.', '')
    # All Remaining Characters must be alphanumeric
    return data_label.isalnum()
