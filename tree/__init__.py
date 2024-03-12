"""The Tree Module.
"""
from input.input_data import InputData


def build_tree(input_data: InputData):
    """
    Build The Tree as defined by the InputData.

    Parameters:
    - input_data (str): The InputData produced by the Input Module.

    Raises:
    SystemExit - If a Tree Validation error occurs.
	"""
    if input_data.is_reversed:
        from tree.tree_validation import validate_trim
        if input_data.data_dir is None:
            instructions = validate_trim(input_data.get_tree_data(), None)
        else:
            instructions = validate_trim(input_data.get_tree_data(), input_data.data_dir)
        from tree.tree_trimmer import trim
        results = trim(instructions)
    else:
        from tree.tree_validation import validate_build
        if input_data.data_dir is None:
            instructions = validate_build(input_data.get_tree_data(), None)
        else:
            instructions = validate_build(input_data.get_tree_data(), input_data.data_dir)
        from tree.tree_builder import build
        results = build(instructions)
    print(results)
