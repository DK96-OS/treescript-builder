"""Testing the Tree Module Init Build Tree Method
"""
import pytest

from input.input_data import InputData
from tree import build_tree
import tree


def mock_build_success(arg):
    return (True, )


def mock_build_fail(arg):
    return (False, )


def test_build_tree_single_file_build_succeeds_returns_true():
    input_data = InputData('data.txt', None, False)
    with pytest.MonkeyPatch().context() as c:
        c.setattr(tree.tree_builder, 'build', mock_build_success)
        result = build_tree(input_data)
    assert len(result) == 1
    assert result[0] == True


def test_build_tree_single_file_build_fails_returns_false():
    input_data = InputData('data.txt', None, False)
    with pytest.MonkeyPatch().context() as c:
        c.setattr(tree.tree_builder, 'build', mock_build_fail)
        result = build_tree(input_data)
    assert len(result) == 1
    assert result[0] == False



def test_build_tree_single_file_trim_succeeds_returns_true():
    input_data = InputData('data.txt', None, True)
    with pytest.MonkeyPatch().context() as c:
        c.setattr(tree.tree_trimmer, 'trim', mock_build_success)
        result = build_tree(input_data)
    assert len(result) == 1
    assert result[0] == True


def test_build_tree_single_file_trim_fails_returns_false():
    input_data = InputData('data.txt', None, True)
    with pytest.MonkeyPatch().context() as c:
        c.setattr(tree.tree_trimmer, 'trim', mock_build_fail)
        result = build_tree(input_data)
    assert len(result) == 1
    assert result[0] == False
