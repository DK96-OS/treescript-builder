""" Operations Package Top-Level Module.
 Author: DK96-OS 2024 - 2025
"""
from treescript_builder.data.input_data import InputData
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.operations import file_operations, results


def tree_operations(
    input_data: InputData,
    instructions: tuple[InstructionData, ...],
) -> str:
    """ Execute Tree Operations using InstructionData and InputData options, and process the results into a printable string.

**Parameters:**
 - input_data (InputData): The InputData options provided by the Input Package.
 - instructions (tuple[InstructionData]): The set of Instructions obtained from Tree Validation.

**Returns:**
 str - The Results, after processing into a printable string.
    """
    return results.process_build_results(
        instructions_tuple=instructions,
        results_tuple=file_operations.build(
            instructions=instructions,
            move_files=input_data.move_files,
            control_mode=input_data.control_mode,
            is_trim=input_data.trim_tree,
        ),
        is_trim=input_data.trim_tree,
        control_mode=input_data.control_mode,
        verbosity_level=input_data.verbosity_level,
    )
