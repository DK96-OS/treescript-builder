"""Testing Input Data.
"""
from treescript_builder.data.tree_data import TreeData
from treescript_builder.input.input_data import InputData
from treescript_builder.input.line_reader import read_input_tree


def test_get_tree_data_single_dir_returns_data():
    i = InputData('src/', None, False)
    gen = read_input_tree(i.tree_input)
    assert list(gen) == [TreeData(1, 0, True, 'src', '')]


def test_get_tree_data_file_in_dir_returns_data():
    i = InputData('src/\n  data.txt', None, False)
    gen = read_input_tree(i.tree_input)
    assert list(gen) == [TreeData(1, 0, True, 'src', ''), TreeData(2, 1, False, 'data.txt', '')]