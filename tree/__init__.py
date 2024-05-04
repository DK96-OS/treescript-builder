"""The Tree Module.
"""
from input.input_data import InputData


def build_tree(input_data: InputData) -> tuple[bool, ...]:
    """
    Build The Tree as defined by the InputData.

    Parameters:
    - input_data (str): The InputData produced by the Input Module.

    Raises:
    SystemExit - If a Tree Validation error occurs.
	"""
    if input_data.is_reversed:
        from tree.trim_validation import validate_trim
        instructions = validate_trim(
            input_data.get_tree_data(),
            input_data.data_dir
        )
        from tree.tree_trimmer import trim
        results = trim(instructions)
    else:
        from tree.build_validation import validate_build
        instructions = validate_build(
            input_data.get_tree_data(),
            input_data.data_dir
        )
        from tree.tree_builder import build
        results = build(instructions)
    #
    return results


def process_results(results: tuple[bool, ...]) -> str:
    """
    Process and Summarize the Results.

    Parameters:
    - results (tuple[bool]): A tuple containing the results of the operations.

    Returns:
    str - A summary of the number of operations that succeeded.
    """
    
    if (length := len(results)) == 0:
        return 'No operations ran.'
    success = sum(iter(results))
    if success == 0:
        return f"All {length} operations failed."
    elif success == length:
        return f"All {length} operations succeeded."
    else:
        return f"{success} out of {length} operations succeeded: {round(100 * success / length, 1)}%"
