"""The Tree Module.
"""
from input.input_data import InputData
from tree.instruction_data import InstructionData


def build_tree(input_data: InputData):
    """
    Build The Tree as defined by the InputData.

    Parameters:
    - input_data (str): The InputData produced by the Input Module.

    Raises:
    SystemExit - If a Tree Validation error occurs.
	"""
    if input_data.is_reversed:
        from tree.tree_trimmer import validate_trim, validate_trim_with_data, trim
        if input_data.data_dir is None:
            instructions = validate_trim(input_data.get_tree_data())
        else:
            instructions = validate_trim_with_data(input_data.get_tree_data(), input_data.data_dir)
        results = trim(instructions)
    else:
        from tree.tree_builder import validate_build, validate_build_with_data, build
        if input_data.data_dir is None:
            instructions = validate_build(input_data.get_tree_data())
        else:
            instructions = validate_build_with_data(input_data.get_tree_data, input_data.data_dir)
        results = build(instructions)
    print(results)
