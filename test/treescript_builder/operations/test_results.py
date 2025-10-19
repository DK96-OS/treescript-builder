""" Testing the Process Results Method. 
 - The Process Results Method is run after the Build or Trim Operations have completed.
 - Results are a tuple of boolean values, where each value corresponds to an input instruction.
 - Previously, it was expected that all results should be True, except in OSError cases.
 - Now, with new FileMode Operations, the user should expect to review the results when using specific FileModes.
 - For example, the Cancel FileMode will prevent file operations if any data loss is expected to occur.
 - This FileMode allows files to be created, but will not overwrite or modify any existing file contents.
 - In this specific FileMode, it is necessary to notify the user of every file operation that was cancelled.
"""
from pathlib import Path

import pytest

from test.treescript_builder.conftest import get_control_mode_text_merge, get_control_mode_write, \
    get_basic_data_tree_instructions
from test.treescript_builder.tree.conftest import generate_simple_tree_instructions, \
    generate_gradle_module_tree_instructions_with_data
from treescript_builder.data.instruction_data import InstructionData
from treescript_builder.operations import results
from treescript_builder.operations.results import process_build_results


@pytest.mark.parametrize(
    'control_mode', [
        # Write ControlMode
        (get_control_mode_write(),),
        (get_control_mode_write(overwrite=True),),
        (get_control_mode_write(overwrite=True, exact=True),),
        (get_control_mode_write(continue_build=True),),
        (get_control_mode_write(overwrite=True, continue_build=True),),
        (get_control_mode_write(overwrite=True, exact=True, continue_build=True),),
        (get_control_mode_write(validate=True),),
        # Text Merge ControlMode
        (get_control_mode_text_merge(is_prepend=False),),
        (get_control_mode_text_merge(is_prepend=False, continue_build=True),),
        (get_control_mode_text_merge(is_prepend=True),),
        (get_control_mode_text_merge(is_prepend=True, continue_build=True),),
    ]
)
def test_process_build_results_empty_instruction_tuple_verbosity_zero_returns_empty(control_mode):
    assert '' == process_build_results(
        instructions_tuple=tuple(),
        results_tuple=tuple(),
        control_mode=control_mode[0],
        move_files=False,
        is_trim=False,
        verbosity_level=0,
    )


@pytest.mark.parametrize(
    'control_mode', [
        # Write ControlMode
        (get_control_mode_write(),),
        (get_control_mode_write(overwrite=True),),
        (get_control_mode_write(overwrite=True, exact=True),),
        (get_control_mode_write(continue_build=True),),
        (get_control_mode_write(overwrite=True, continue_build=True),),
        (get_control_mode_write(overwrite=True, exact=True, continue_build=True),),
        (get_control_mode_write(validate=True),),
        # Text Merge ControlMode
        (get_control_mode_text_merge(is_prepend=False),),
        (get_control_mode_text_merge(is_prepend=False, continue_build=True),),
        (get_control_mode_text_merge(is_prepend=True),),
        (get_control_mode_text_merge(is_prepend=True, continue_build=True),),
    ]
)
def test_process_build_results_basic_data_tree_result_true_verbosity_zero_returns_empty(control_mode):
    assert '' == process_build_results(
        instructions_tuple=get_basic_data_tree_instructions(),
        results_tuple=(True, True),
        control_mode=control_mode[0],
        move_files=False,
        is_trim=False,
        verbosity_level=0,
    )


@pytest.mark.parametrize(
    'control_mode', [
        # Write ControlMode
        (get_control_mode_write(),),
        (get_control_mode_write(overwrite=True),),
        (get_control_mode_write(overwrite=True, exact=True),),
        (get_control_mode_write(continue_build=True),),
        (get_control_mode_write(overwrite=True, continue_build=True),),
        (get_control_mode_write(overwrite=True, exact=True, continue_build=True),),
        (get_control_mode_write(validate=True),),
        # Text Merge ControlMode
        (get_control_mode_text_merge(is_prepend=False),),
        (get_control_mode_text_merge(is_prepend=False, continue_build=True),),
        (get_control_mode_text_merge(is_prepend=True),),
        (get_control_mode_text_merge(is_prepend=True, continue_build=True),),
    ]
)
def test_process_build_results_empty_tuple_verbosity_1_returns_no_file_operations(control_mode):
    assert results._NO_FILETREE_OPERATIONS == process_build_results(
        instructions_tuple=tuple(),
        results_tuple=tuple(),
        control_mode=control_mode[0],
        move_files=False,
        is_trim=False,
        verbosity_level=1,
    )


@pytest.mark.parametrize(
    'control_mode', [
        # Write ControlMode
        (get_control_mode_write(),),
        (get_control_mode_write(overwrite=True),),
        (get_control_mode_write(overwrite=True, exact=True),),
        (get_control_mode_write(continue_build=True),),
        (get_control_mode_write(overwrite=True, continue_build=True),),
        (get_control_mode_write(overwrite=True, exact=True, continue_build=True),),
        (get_control_mode_write(validate=True),),
        # Text Merge ControlMode
        (get_control_mode_text_merge(is_prepend=False),),
        (get_control_mode_text_merge(is_prepend=False, continue_build=True),),
        (get_control_mode_text_merge(is_prepend=True),),
        (get_control_mode_text_merge(is_prepend=True, continue_build=True),),
    ]
)
def test_process_build_results_empty_tuple_verbosity_2_returns_no_file_operations(control_mode):
    assert results._NO_FILETREE_OPERATIONS == process_build_results(
        instructions_tuple=tuple(),
        results_tuple=tuple(),
        control_mode=control_mode[0],
        move_files=False,
        is_trim=False,
        verbosity_level=2,
    )


@pytest.mark.parametrize(
    'control_mode, expected_result', [
        # Write ControlMode
        (get_control_mode_write(), 'WRITE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_write(validate=True), 'WRITE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_write(continue_build=True), 'WRITE, CONTINUE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_write(overwrite=True), 'OVERWRITE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_write(overwrite=True, exact=True), 'OVERWRITE-EXACT:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_write(overwrite=True, exact=True, continue_build=True), 'OVERWRITE-EXACT, CONTINUE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_write(overwrite=True, continue_build=True), 'OVERWRITE, CONTINUE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        # Text Merge ControlMode
        (get_control_mode_text_merge(is_prepend=False), 'APPEND:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_text_merge(is_prepend=False, continue_build=True), 'APPEND, CONTINUE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_text_merge(is_prepend=True), 'PREPEND:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
        (get_control_mode_text_merge(is_prepend=True, continue_build=True), 'PREPEND, CONTINUE:\n' + results._SINGLE_OPERATION_SUCCEEDED_MSG),
    ]
)
def test_process_build_results_single_instruction_tuple_pass_verbosity_1_returns_summary(control_mode, expected_result):
    assert expected_result == process_build_results(
        instructions_tuple=(InstructionData(False, Path('src/data.txt'), None), ),
        results_tuple=(True,),
        control_mode=control_mode,
        move_files=False,
        is_trim=False,
        verbosity_level=1,
    )


@pytest.mark.parametrize(
    'control_mode, expected_result', [
        (get_control_mode_text_merge(is_prepend=False), 'APPEND:\nAll 2 operations succeeded.'),
        (get_control_mode_text_merge(is_prepend=False, continue_build=True), 'APPEND, CONTINUE:\nAll 2 operations succeeded.'),
        (get_control_mode_text_merge(is_prepend=True), 'PREPEND:\nAll 2 operations succeeded.'),
        (get_control_mode_text_merge(is_prepend=True, continue_build=True), 'PREPEND, CONTINUE:\nAll 2 operations succeeded.'),
    ]
)
def test_process_build_results_basic_data_tree_text_merge_verbosity_1_returns_(control_mode, expected_result):
    assert expected_result == process_build_results(
        instructions_tuple=get_basic_data_tree_instructions(),
        results_tuple=(True, True),
        control_mode=control_mode,
        move_files=False,
        is_trim=False,
        verbosity_level=1,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result", [
        (0, ''),
        (1, 'APPEND:\nAll 2 operations succeeded.'),
        (2, 'APPEND:\nPass: src/\nPass: src/data.txt\nAll 2 operations succeeded.'),
    ]
)
def test_process_build_results_simple_tree_append_succeeds_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(True, True),
        control_mode=get_control_mode_text_merge(is_prepend=False),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'WRITE:\nAll 2 operations succeeded.'),
        (2, 'WRITE:\nPass: src/\nPass: src/data.txt\nAll 2 operations succeeded.'),
    ]
)
def test_process_build_results_simple_tree_move_succeeds_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(True, True),
        control_mode=get_control_mode_write(),
        move_files=True,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'WRITE:\nFail: src/data.txt\n(1 / 2) operations succeeded: 50.0%'),
        (2, 'WRITE:\nPass: src/\nFail: src/data.txt\n(1 / 2) operations succeeded: 50.0%'),
    ]
)
def test_process_build_results_simple_tree_move_file_fails_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(True, False),
        control_mode=get_control_mode_write(),
        move_files=True,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'OVERWRITE:\nAll 2 operations succeeded.'),
        (2, 'OVERWRITE:\nPass: src/\nPass: src/data.txt\nAll 2 operations succeeded.'),
    ]
)
def test_process_build_results_simple_tree_overwrite_succeeds_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(True, True),
        control_mode=get_control_mode_write(overwrite=True),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'OVERWRITE-EXACT:\nAll 2 operations succeeded.'),
        (2, 'OVERWRITE-EXACT:\nPass: src/\nPass: src/data.txt\nAll 2 operations succeeded.'),
    ]
)
def test_process_build_results_simple_tree_overwrite_exact_succeeds_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(True, True),
        control_mode=get_control_mode_write(overwrite=True, exact=True),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'PREPEND:\nAll 2 operations succeeded.'),
        (2, 'PREPEND:\nPass: src/\nPass: src/data.txt\nAll 2 operations succeeded.'),
    ]
)
def test_process_build_results_simple_tree_prepend_succeeds_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(True, True),
        control_mode=get_control_mode_text_merge(is_prepend=True),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'APPEND:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
        (2, 'APPEND:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
    ]
)
def test_process_build_results_simple_tree_append_fails_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(False, False),
        control_mode=get_control_mode_text_merge(is_prepend=False),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'APPEND, CONTINUE:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
        (2, 'APPEND, CONTINUE:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
    ]
)
def test_process_build_results_simple_tree_append_continue_fails_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(False, False),
        control_mode=get_control_mode_text_merge(is_prepend=False, continue_build=True),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'WRITE:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
        (2, 'WRITE:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
    ]
)
def test_process_build_results_simple_tree_cancel_fails_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(False, False),
        control_mode=get_control_mode_write(),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'WRITE:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
        (2, 'WRITE:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
    ]
)
def test_process_build_results_simple_tree_move_fails_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(False, False),
        control_mode=get_control_mode_write(),
        move_files=True,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'OVERWRITE-EXACT:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
        (2, 'OVERWRITE-EXACT:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
    ]
)
def test_process_build_results_simple_tree_overwrite_fails_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(False, False),
        control_mode=get_control_mode_write(overwrite=True, exact=True),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, expected_result",
    [
        (0, ''),
        (1, 'PREPEND:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
        (2, 'PREPEND:\nFail: src/\nFail: src/data.txt\nAll 2 operations failed.'),
    ]
)
def test_process_build_results_simple_tree_prepend_fails_returns(
    verbosity, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(False, False),
        control_mode=get_control_mode_text_merge(is_prepend=True),
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity,
    )


@pytest.mark.parametrize(
    "verbosity, control_mode, expected_result",
    [
        (0, get_control_mode_text_merge(is_prepend=False), ''),
        (0, get_control_mode_text_merge(is_prepend=False, continue_build=True), ''),
        (0, get_control_mode_text_merge(is_prepend=True), ''),
        (0, get_control_mode_text_merge(is_prepend=True, continue_build=True), ''),
        #
        (1, get_control_mode_text_merge(is_prepend=False), 'APPEND:\nFail: src/data.txt\n(1 / 2) operations succeeded: 50.0%'),
        (1, get_control_mode_text_merge(is_prepend=True), 'PREPEND:\nFail: src/data.txt\n(1 / 2) operations succeeded: 50.0%'),
        #
        (2, get_control_mode_text_merge(is_prepend=False), 'APPEND:\nPass: src/\nFail: src/data.txt\n(1 / 2) operations succeeded: 50.0%'),
        (2, get_control_mode_text_merge(is_prepend=True), 'PREPEND:\nPass: src/\nFail: src/data.txt\n(1 / 2) operations succeeded: 50.0%'),
    ]
)
def test_process_build_results_simple_tree_text_merge_half_succeeded_returns_message(
    verbosity, control_mode, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_simple_tree_instructions()),
        results_tuple=(True, False),
        control_mode=control_mode,
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity
    )


@pytest.mark.parametrize(
    "verbosity, control_mode, expected_result",
    [
        (0, get_control_mode_text_merge(is_prepend=False), ''),
        (0, get_control_mode_text_merge(is_prepend=False, continue_build=True), ''),
        (0, get_control_mode_text_merge(is_prepend=True), ''),
        (0, get_control_mode_text_merge(is_prepend=True, continue_build=True), ''),
        #
        (1, get_control_mode_text_merge(is_prepend=False), 'APPEND:\nFail: module1/src/main/java/\nFail: module1/src/test/java/\n(2 / 4) operations succeeded: 50.0%'),
        (1, get_control_mode_text_merge(is_prepend=True), 'PREPEND:\nFail: module1/src/main/java/\nFail: module1/src/test/java/\n(2 / 4) operations succeeded: 50.0%'),
        #
        (2, get_control_mode_text_merge(is_prepend=False), 'APPEND:\nPass: module1/\nPass: module1/build.gradle\nFail: module1/src/main/java/\nFail: module1/src/test/java/\n(2 / 4) operations succeeded: 50.0%'),
        (2, get_control_mode_text_merge(is_prepend=True), 'PREPEND:\nPass: module1/\nPass: module1/build.gradle\nFail: module1/src/main/java/\nFail: module1/src/test/java/\n(2 / 4) operations succeeded: 50.0%'),
    ]
)
def test_process_build_results_data_tree_text_merge_half_succeeded_returns_message(
    verbosity, control_mode, expected_result
):
    assert expected_result == process_build_results(
        instructions_tuple=tuple(generate_gradle_module_tree_instructions_with_data()),
        results_tuple=(True, True, False, False),
        control_mode=control_mode,
        move_files=False,
        is_trim=False,
        verbosity_level=verbosity
    )
