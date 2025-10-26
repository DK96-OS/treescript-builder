""" Operations Package Top-Level Module.
 Author: DK96-OS 2024 - 2025
"""
from treescript_builder.data.input_data import InputData
from treescript_builder.operations.file_operations import build
from treescript_builder.operations.results import process_build_results
from treescript_builder.tree import validate_tree


def tree_operations(
    input_data: InputData,
) -> str:
    """ Execute Tree Operations using InstructionData and InputData options, and process the results into a printable string.

**Parameters:**
 - input_data (InputData): The InputData options provided by the Input Package.

**Returns:**
 str - The results of the operation as a printable string.
    """
    instructions = validate_tree(input_data)
    results = build(
        instructions=instructions,
        move_files=input_data.move_files,
        control_mode=input_data.control_mode,
        is_trim=input_data.trim_tree,
    )
    return process_build_results(
        instructions_tuple=instructions,
        results_tuple=results,
        move_files=input_data.move_files,
        is_trim=input_data.trim_tree,
        control_mode=input_data.control_mode,
        verbosity_level=input_data.verbosity_level,
    )
