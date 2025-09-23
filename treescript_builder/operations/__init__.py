""" Operations Package Top-Level Module.
 Author: DK96-OS 2024 - 2025
"""
from treescript_builder.data.input_data import InputData
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.operations import file_builder, file_trimmer, results


def tree_operations(
    input_data: InputData,
    instructions: tuple[InstructionData, ...],
) -> tuple[bool, ...]:
    """ 
    """
    return file_trimmer.trim(
        instructions, input_data.move_files, input_data.control_mode
    ) if input_data.trim_tree else file_builder.build(
        instructions, input_data.move_files, input_data.control_mode
    )


def operate_with_results(
    input_data: InputData,
    instructions: tuple[InstructionData, ...],
) -> str:
    """ 
    """
    return results.process_build_results(
        instructions,
        tree_operations(input_data, instructions),
        input_data.control_mode,
        input_data.verbosity_level,
    )
