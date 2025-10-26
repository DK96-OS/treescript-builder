""" The Tree Package Top-Level Module.
"""
from treescript_builder.data.input_data import InputData
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.tree import build_validation, line_reader, trim_validation


def validate_tree(
    input_data: InputData,
) -> tuple[InstructionData,...]:
    """ Build The Tree as defined by the InputData.
 - Provides both Trim and Build Validated Instructions, depending on InputData.trim_tree.
 - Validation is handled in separate modules: build_validation, and trim_validation.

**Parameters:**
 - input_data (str): The InputData provided by the Input Package. Contains InputTree and options, notably trim_tree..

**Returns:**
 tuple[InstructionData,...] - A resulting set of Instruction Data, produced by a valid Input Tree..

**Raises:**
 SystemExit - If a Tree Validation error occurs.
	"""
    tree_generator = line_reader.read_input_tree(input_data.tree_input)
    return trim_validation.validate_trim(
        tree_generator, input_data.data_dir, input_data.move_files,
    ) if input_data.trim_tree else build_validation.validate_build(
        tree_generator, input_data.data_dir
    )
