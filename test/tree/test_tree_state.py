"""Testing Tree State.
"""
import pytest

from tree.tree_state import TreeState


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
    assert instance.process_queue() == None


def test_process_queue_single_item_queue_():
    instance = TreeState()
    instance.add_to_queue('src')
    assert instance.process_queue() == './src/'


def test_process_queue_multi_item_queue_():
    instance = TreeState()
    instance.add_to_queue('src')
    instance.add_to_queue('main')
    instance.add_to_queue('java')
    assert instance.process_queue() == './src/main/java/'


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
