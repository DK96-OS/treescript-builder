""" Testing Tree State.
"""
from pathlib import Path

import pytest

from treescript_builder.data.tree_data import TreeData
from treescript_builder.data.tree_state import TreeState


def test_validate_tree_data_first_dir_returns_0():
    input_data = TreeData(1, 0, True, 'src', '')
    instance = TreeState()
    assert instance.validate_tree_data(input_data) == 0
    assert instance._prev_line_number == 1


def test_validate_tree_data_invalid_line_number_raises_exit():
    input_data = TreeData(0, 0, True, 'src', '')
    instance = TreeState()
    with pytest.raises(SystemExit):
        instance.validate_tree_data(input_data)


def test_validate_tree_data_item_in_queue_returns_0():
    instance = TreeState()
    instance.add_to_queue('src')
    # initial_data = TreeData(1, 0, True, 'src', '')
    input_data = TreeData(2, 1, True, 'main', '')
    assert instance.validate_tree_data(input_data) == 0
    assert instance._prev_line_number == 2


def test_validate_tree_data_item_in_stack_returns_0():
    instance = TreeState()
    instance.add_to_stack('src')
    # initial_data = TreeData(1, 0, True, 'src', '')
    input_data = TreeData(2, 1, True, 'main', '')
    assert instance.validate_tree_data(input_data) == 0
    assert instance._prev_line_number == 2


def test_validate_tree_data_decrease_depth_returns_negative():
    instance = TreeState()
    instance.add_to_stack('src')
    # initial_data = TreeData(1, 0, True, 'src', '')
    input_data = TreeData(2, 0, True, 'test', '')
    assert instance.validate_tree_data(input_data) == -1
    assert instance._prev_line_number == 2


@pytest.mark.parametrize(
    'depth',
    [
        1, 2, -1
    ]
)
def test_validate_tree_data_invalid_depth_raises_exit(depth):
    input_data = TreeData(1, depth, True, 'src', '')
    instance = TreeState()
    with pytest.raises(SystemExit):
        instance.validate_tree_data(input_data)


def test_get_current_path_():
    instance = TreeState()
    assert instance.get_current_path() == Path('./')


def test_get_current_path_single_item_stack():
    instance = TreeState()
    instance.add_to_stack('src')
    assert instance.get_current_path() == Path('./src/')


def test_get_current_path_single_item_queue():
    instance = TreeState()
    instance.add_to_queue('src')
    assert instance.get_current_path() == Path('./src/')


@pytest.mark.parametrize(
    'test_input',
    [
        (('src')),
        (('src', 'main')),
        (('src', 'main', 'java')),
    ]
)
def test_add_to_queue_empty_stack_increases_depth(test_input):
    instance = TreeState()
    for dir in test_input:
        instance.add_to_queue(dir)
    assert instance.get_current_depth() == len(test_input)


@pytest.mark.parametrize(
    'test_input',
    [
        (('src')),
        (('src', 'main')),
        (('src', 'main', 'java')),
    ]
)
def test_add_to_stack_empty_stack_increases_depth(test_input):
    instance = TreeState()
    for dir in test_input:
        instance.add_to_stack(dir)
    assert instance.get_current_depth() == len(test_input)


@pytest.mark.parametrize(
    'test_input',
    [
        (('main')),
        (('main', 'java')),
    ]
)
def test_add_to_queue_nonempty_stack_increases_depth(test_input):
    instance = TreeState()
    instance.add_to_stack('src')
    for dir in test_input:
        instance.add_to_queue(dir)
    assert instance.get_current_depth() == 1 + len(test_input)


def test_process_queue_empty_queue_returns_none():
    instance = TreeState()
    assert instance.process_queue() is None


def test_process_queue_single_item_queue_():
    instance = TreeState()
    instance.add_to_queue('src')
    assert instance.process_queue() == Path('./src/')


def test_process_queue_multi_item_queue_():
    instance = TreeState()
    instance.add_to_queue('src')
    instance.add_to_queue('main')
    instance.add_to_queue('java')
    assert instance.process_queue() == Path('./src/main/java/')


def test_process_stack_negative_depth_raises_exit():
    instance = TreeState()
    with pytest.raises(SystemExit):
        tuple(iter(instance.process_stack(-1)))


def test_process_stack_empty_depth_0_yields_nothing():
    instance = TreeState()
    assert len(tuple(iter(instance.process_stack(0)))) == 0


def test_process_stack_empty_depth_1_yields_nothing():
    instance = TreeState()
    assert len(tuple(iter(instance.process_stack(0)))) == 0


def test_process_stack_single_item_depth_0_yields_item():
    instance = TreeState()
    instance.add_to_stack('src')
    assert len(tuple(iter(instance.process_stack(0)))) == 1


def test_process_stack_single_item_depth_1_yields_nothin():
    instance = TreeState()
    instance.add_to_stack('src')
    assert len(tuple(iter(instance.process_stack(1)))) == 0


@pytest.mark.parametrize(
    'test_input,expect',
    [
        (0, True),
        (1, False),
        (-1, False),
        (10, False),
    ]
)
def test_reduce_depth_empty_stack_returns_bool(test_input, expect):
    instance = TreeState()
    assert instance.reduce_depth(test_input) == expect


@pytest.mark.parametrize(
    'test_input,expect',
    [
        (0, True),
        (1, True),
        (2, True),
        (3, True),
        (-1, False),
        (10, False),
    ]
)
def test_reduce_depth_single_item_stack_returns_bool(test_input, expect):
    instance = TreeState()
    instance.add_to_stack('src')
    instance.add_to_stack('main')
    instance.add_to_stack('java')
    assert instance.reduce_depth(test_input) == expect