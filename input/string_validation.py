"""String Validation Methods.
"""


def validate_name(argument) -> bool:
    """
    Determine whether an argument is a non-empty string.
        Does not count whitespace.
        Uses the strip method to remove empty space.

    Parameters:
    - argument (str) : The given argument.

    Returns:
    bool - True if the argument qualifies as valid.
    """
    if argument is None or not isinstance(argument, str):
        return False
    elif len(argument.strip()) < 1:
        return False
    return True


def validate_data_label(data_label: str) -> bool:
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
