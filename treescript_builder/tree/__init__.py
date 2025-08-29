""" The Tree Package Top-Level Module.
"""
from treescript_builder.data.input_data import InputData
from treescript_builder.tree.line_reader import read_input_tree
from treescript_builder.operations.results import process_build_results, process_trim_results


def build_tree(input_data: InputData) -> str:
    """ Build The Tree as defined by the InputData.

**Parameters:**
 - input_data (str): The InputData produced by the Input Module.

**Returns:**
 str - A result summary string, consistent with the InputData verbosity_level attribute.

**Raises:**
 SystemExit - If a Tree Validation error occurs.
	"""
    if input_data.trim_tree:
        return _validate_and_trim(input_data)
    return _validate_and_build(input_data)


def _validate_and_build(in_data: InputData) -> str:
    from treescript_builder.tree.build_validation import validate_build
    instructions = validate_build(
        read_input_tree(in_data.tree_input),
        in_data.data_dir
    )
    from treescript_builder.operations.file_builder import build
    return process_build_results(
        instructions,
        results_tuple=build(instructions, in_data.mode),
        file_mode=in_data.mode,
        verbosity_level=in_data.verbosity_level
    )


def _validate_and_trim(in_data: InputData) -> str:
    from treescript_builder.tree.trim_validation import validate_trim
    instructions = validate_trim(
        read_input_tree(in_data.tree_input),
        in_data.data_dir
    )
    from treescript_builder.operations.file_trimmer import trim
    return process_trim_results(
        instructions,
        results_tuple=trim(instructions, in_data.mode),
        file_mode=in_data.mode,
        verbosity_level=in_data.verbosity_level
    )
