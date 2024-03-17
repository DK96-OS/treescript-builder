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


def validate_dir_name(dir_name: str, fwd_slash: bool) -> str | None:
    """
    Determine that a directory is correctly formatted.
        This method should be called once for each slash type.

    Parameters:
    - dir_name (str): The given input to be validated.

    Returns:
    str | None - The valid directory name, or none.

    Raises:
    ValueError - 
    """
    # Test one of the slashes
    slash = '/' if fwd_slash else '\\'
    if slash not in dir_name:
        return None
    # Check for slash characters
    if dir_name.endswith(slash) or dir_name.startswith(slash):
        name = dir_name.strip(slash)
        # Check for internal slash characters
        if slash in name:
            raise ValueError('Multi-dir line detected')
    else:
        # Found slash chars only within the node name (multi-dir line)
        raise ValueError('Multi-dir line detected')
    if len(name) == 0:
        raise ValueError('The name is empty')
    # todo: Check for illegal characters (parent dir, current dir)
    return (True, name)
