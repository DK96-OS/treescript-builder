""" TS-Builder Results Processing and Summarization.
"""
from typing import Generator

from treescript_builder.data.control_modes import ControlMode, WriteControlModes, TextMergeControlModes
from treescript_builder.data.instruction_data import InstructionData


def process_build_results(
    instructions_tuple: tuple[InstructionData, ...],
    results_tuple: tuple[bool, ...],
    control_mode: ControlMode,
    move_files: bool,
    is_trim: bool,
    verbosity_level: int,
) -> str:
    """ Process the Build operations Results, and produce an output string that summarizes results according to verbosity level.

**Parameters:**
 - instructions_tuple (tuple[InstructionData, ...]): The instructions that were executed during FileTree Operations.
 - results_tuple (tuple[bool, ...]): A tuple containing the results of the operations.
 - control_mode (ControlMode): The options for controlling detailed operation behaviours.
 - move_files (bool): Whether to move files in the operation, rather than copy.
 - is_trim (bool): Whether the FileTree Operation was Trim instead of Build.
 - verbosity_level (int): The level describing the amount of information to be included.

**Returns:**
 str - A summary of the operations.

**Raises:**
 TypeError - If any argument is not the correct Type.
 ValueError - If the lengths of the Tuples do not match.
    """
    if not isinstance(instructions_tuple, tuple) or \
            not isinstance(results_tuple, tuple) or \
            not (isinstance(control_mode, WriteControlModes) or isinstance(control_mode, TextMergeControlModes)) or \
            not isinstance(move_files, bool) or \
            not isinstance(is_trim, bool) or \
            not isinstance(verbosity_level, int):
        raise TypeError
    if verbosity_level < 1:   # No Output
        return ''
    if len(instructions_tuple) != len(results_tuple):
        raise ValueError(_INVALID_RESULTS_TUPLE_MSG)
    if len(results_tuple) == 0:
        return _NO_FILETREE_OPERATIONS
    # Results Summary.
    return _create_opening_statement(control_mode, is_trim, move_files) + "\n" + _verbose_file_paths(
        verbosity=verbosity_level,
        instructions_tuple=instructions_tuple,
        results_tuple=results_tuple,
    ) + _percentage_summary(results_tuple)


_NO_FILETREE_OPERATIONS = 'No FileTree Operations Ran.'
_INVALID_RESULTS_TUPLE_MSG = 'Inconsistent Instruction and Results Tuple Lengths.'

_PASSED_OPERATION_MSG = 'Pass: '
_FAILED_OPERATION_MSG = 'Fail: '

_SINGLE_OPERATION_SUCCEEDED_MSG = 'File Operation Succeeded.'
_SINGLE_OPERATION_FAILED_MSG = 'File Operation Failed.'
_ALL_OPERATION_SUCCEEDED_MSG = 'All File Operations Succeeded.'
_ALL_OPERATION_FAILED_MSG = 'All File Operations Failed.'


def _wrap_text_block_in_newline(
    block_text: str,
) -> str:
    """ The benefit of this method is that if the given str is empty, there is no new line. """
    return block_text + ('\n' if 0 < len(block_text) else '')


def _filter_instruction_results(
    instructions_tuple: tuple[InstructionData, ...],
    results_tuple: tuple[bool, ...],
    is_true: bool,
) -> Generator[InstructionData, None, None]:
    """ Filter InstructionData against corresponding True or False Results. """
    filter_func = (lambda enumerated_result: enumerated_result[1]) if is_true else (lambda enumerated_result: not enumerated_result[1])
    for x in filter(filter_func, enumerate(results_tuple)):
        yield instructions_tuple[x[0]]


def _verbose_file_paths(
    verbosity: int,
    instructions_tuple: tuple[InstructionData, ...],
    results_tuple: tuple[bool, ...],
) -> str:
    """ This method extracts information from the results of a set of file tree operations.

**Parameters:**
 - verbosity (int): The Key Value in determining the selection of files to include in the output.
 - instructions_tuple (tuple[InstructionData, ...]): The tuple containing the Instructions to be processed in the results.
 - results_tuple (tuple[bool, ...]): The tuple containing the file operation status for each Instruction.

**Returns:**
 str - The output string containing the requested information from the InstructionData-Results data input.
    """
    if verbosity == 1: # Only Failed File Operations + Summary of Operations Statement.
        return _wrap_text_block_in_newline(
            '\n'.join(
                _FAILED_OPERATION_MSG + str(x.path) + ('/' if x.is_dir else '')
                for x in _filter_instruction_results(instructions_tuple, results_tuple, is_true=False)
            )
        )
    else:  # Opening Statement + All File Paths + Summary of Operations Statement
        pass_files = _wrap_text_block_in_newline(
            '\n'.join(
                _PASSED_OPERATION_MSG + str(x.path) + ('/' if x.is_dir else '')
                for x in _filter_instruction_results(instructions_tuple, results_tuple, is_true=True)
            )
        )
        failed_files = _wrap_text_block_in_newline(
            '\n'.join(map(
                lambda x: _FAILED_OPERATION_MSG + str(x.path) + ('/' if x.is_dir else ''),
                _filter_instruction_results(instructions_tuple, results_tuple, is_true=False)
            ))
        )
        return pass_files + failed_files


def _create_opening_statement(
    control_mode: ControlMode,
    is_trim: bool, #unused
    move_files: bool, #unused
) -> str:
    if isinstance(control_mode, WriteControlModes):
        return _get_write_mode_segment(control_mode)
    elif isinstance(control_mode, TextMergeControlModes):
        merge_segment = "PREPEND" if control_mode.prepend_merge else "APPEND"
        if control_mode.continue_build:
            merge_segment += ', CONTINUE'
        return merge_segment + ':'
    else:
        raise TypeError


def _get_write_mode_segment(write_mode: WriteControlModes):
    if write_mode.overwrite:
        ow_segment = "OVERWRITE"
        if write_mode.exact_build:
            ow_segment += "-EXACT"
        if write_mode.continue_build:
            return ow_segment + ", CONTINUE:"
        return ow_segment + ":"
    if write_mode.continue_build:
        return "WRITE, CONTINUE:"
    return "WRITE:"


def _percentage_summary(
    results_tuple: tuple[bool, ...],
) -> str:
    if (length := len(results_tuple)) == 0:
        return _NO_FILETREE_OPERATIONS
    elif (success := sum(results_tuple)) == 0:
        return _SINGLE_OPERATION_FAILED_MSG if length == 1 else _ALL_OPERATION_FAILED_MSG
    elif success == length:
        return _SINGLE_OPERATION_SUCCEEDED_MSG if length == 1 else _ALL_OPERATION_SUCCEEDED_MSG
    # Compute the Fraction of success operations
    return f"({success} / {length}) Operations Succeeded: {round(100 * success / length, 1)}%"
