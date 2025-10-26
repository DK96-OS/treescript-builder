""" Testing Input Data.
"""
from treescript_builder.data.input_data import InputData
from treescript_builder.data.tree_data import TreeData
from treescript_builder.tree.line_reader import read_input_tree


def test_get_tree_data_single_dir_returns_data(control_trywrite):
    i = InputData('src/', None, False, False, control_trywrite, 0)
    gen = read_input_tree(i.tree_input)
    assert list(gen) == [
        TreeData(1, 0, True, 'src', '')
    ]


def test_get_tree_data_file_in_dir_returns_data(control_trywrite):
    i = InputData('src/\n  data.txt', None, False, False, control_trywrite, 0)
    gen = read_input_tree(i.tree_input)
    assert list(gen) == [
        TreeData(1, 0, True, 'src', ''),
        TreeData(2, 1, False, 'data.txt', '')
    ]
