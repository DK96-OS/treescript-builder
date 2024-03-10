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
    instructions = _process_input(input_data)
    #
    if input_data.is_reversed:
        from tree.tree_trimmer import trim
        results = trim(instructions)
    else:
        from tree.tree_builder import build
        results = build(instructions)
    # todo: Process Results


def _process_input(input_data: InputData) -> tuple[InstructionData]:
    """
    Process Input Tree Data into Instruction Data.
        Validates Tree operations to catch errors before execution.

    Parameters:
    - input_data (InputData): The Input given to the module.

    Returns:
    tuple[InstructionData] - The set of Instructions to execute.
    """
    tree_data = input_data.get_tree_data()
    #
    if input_data.data_dir is None:
        from tree.tree_validation import validate_tree
        return validate_tree(tree_data)
    else:
        from tree.tree_validation import validate_with_data_dir
        return validate_with_data_dir(
            tree_data, input_data.data_dir
        )
