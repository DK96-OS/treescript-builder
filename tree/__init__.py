"""The Tree Module.
"""
from input import InputData


def build_tree(input_data: InputData):
    """
    Build The Tree as defined by the InputData.

    Parameters:
    - input_data (str): The InputData produced by the Input Module.

    Raises:
    SystemExit
	"""
    if input_data.is_reversed:
        from tree_trimmer import trim
        trim(input_data)
    else:
        from tree_builder import build
        build(input_data)
