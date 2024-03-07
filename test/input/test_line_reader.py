import pytest
from input.line_reader import _calculate_depth, _process_line, read_input_tree, read_input_tree_to_tuple
from input.tree_data import TreeData
from test.input import create_depth


# Directory Variants: A tuple of all possible ways that a directory may be represented.
dir_variants = ('/dir', 'dir/', '\\dir', 'dir\\')


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + 'file', depth)
        for depth in range(0, 9)
    ]
)
def test_calculate_depth_file_returns_true(test_input, expect):
    assert _calculate_depth(test_input) == expect


@pytest.mark.parametrize(
    "test_input", 
    [
        (create_depth(depth) + ' file')
        for depth in range(0, 9)
    ]
)
def test_calculate_depth_file_odd_spaces_raises_exit(test_input):
    assert _calculate_depth(test_input) == -1


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + dir, depth)
        for dir in dir_variants
        for depth in range(0, 9)
    ]
)
def test_calculate_depth_dir_returns_true(test_input, expect):
    assert _calculate_depth(test_input) == expect


@pytest.mark.parametrize(
    "test_input", 
    [
        (create_depth(depth) + ' ' + dir)
        for dir in dir_variants
        for depth in range(0, 9)
    ]
)
def test_calculate_depth_dir_odd_spaces_returns_negative(test_input):
    assert _calculate_depth(test_input) == -1


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + 'file', TreeData(1, depth, False, 'file', ''))
        for depth in range(0, 4)
    ]
)
def test_process_line_file_returns_data(test_input, expect):
    assert _process_line(1, test_input) == expect


@pytest.mark.parametrize(
    "test_input", 
    [
        (create_depth(depth) + ' ' + 'file')
        for depth in range(0, 4)
    ]
)
def test_process_line_file_odd_spaces_raises_exit(test_input):
    try:
        _process_line(1, test_input)
        assert False
    except SystemExit as e:
        assert True


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + 'file DataLabel', TreeData(1, depth, False, 'file', 'DataLabel'))
        for depth in range(0, 4)
    ]
)
def test_process_line_file_data_label_returns_data(test_input, expect):
    assert _process_line(1, test_input) == expect


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + 'file ', TreeData(1, depth, False, 'file', ''))
        for depth in range(0, 4)
    ]
)
def test_process_line_file_trailing_space_returns_data(test_input, expect):
    assert _process_line(1, test_input) == expect


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + dir, TreeData(1, depth, True, dir.strip('/\\'), ''))
        for dir in dir_variants
        for depth in range(0, 4)
    ]
)
def test_process_line_dir_returns_data(test_input, expect):
    assert _process_line(1, test_input) == expect


@pytest.mark.parametrize(
    "test_input", 
    [
        (create_depth(depth) + ' ' + dir)
        for dir in dir_variants
        for depth in range(0, 4)
    ]
)
def test_process_line_dir_odd_spaces_raises_exit(test_input):
    try:
        _process_line(1, test_input)
        assert False
    except SystemExit as e:
        assert True


def test_read_input_tree_all_dirs():
    test_input = """
src/
  data/
      more_data/
"""
    generator = read_input_tree(test_input)
    assert next(generator) == TreeData(2, 0, True, 'src', '')
    assert next(generator) == TreeData(3, 1, True, 'data', '')
    assert next(generator) == TreeData(4, 2, True, 'more_data', '')
    try:
        next(generator)
        assert False
    except StopIteration as e:
        assert True


def test_read_input_tree_files_including_comment_yields_data():
    test_input = """src/
  data.txt
  # comment
  more_data.txt Label
"""
    generator = read_input_tree(test_input)
    assert next(generator) == TreeData(1, 0, True, 'src', '')
    assert next(generator) == TreeData(2, 1, False, 'data.txt', '')
    assert next(generator) == TreeData(4, 1, False, 'more_data.txt', 'Label')
    try:
        next(generator)
        assert False
    except StopIteration as e:
        assert True


def test_read_input_tree_trailing_blank_lines_are_ignored():
    test_input = """
src/
  data.txt
  
    """
    generator = read_input_tree(test_input)
    assert next(generator) == TreeData(2, 0, True, 'src', '')
    assert next(generator) == TreeData(3, 1, False, 'data.txt', '')
    # All Remaining Lines are blank and should be ignored
    try:
        next(generator)
        assert False
    except StopIteration as e:
        assert True


def test_read_input_tree_nameless_dir_raise_exit():
    test_input = """
src/
  data.txt
  /
    """
    generator = read_input_tree(test_input)
    assert next(generator) == TreeData(2, 0, True, 'src', '')
    assert next(generator) == TreeData(3, 1, False, 'data.txt', '')
    # The next line is a dir slash with no name
    try:
        next(generator)
        assert False
    except SystemExit as e:
        assert True


@pytest.mark.parametrize(
    'test_input',
    [
        "src/\n  data.txt\n  ../\n    ../\n",
        "src/\n  data.txt\n  ../../\n",
        "src/\n  data.txt\n  ./\n",
    ]
)
def test_read_input_tree_dir_escape_raise_exit(test_input):
    generator = read_input_tree(test_input)
    assert next(generator) == TreeData(1, 0, True, 'src', '')
    assert next(generator) == TreeData(2, 1, False, 'data.txt', '')
    # The next line is a forbidden symbolic link
    try:
        next(generator)
        assert False
    except SystemExit as e:
        assert True


@pytest.mark.parametrize(
    'test_input',
    [
        "src/\n main/",
        "src/\n data.txt",
    ]
)
def test_read_input_tree_odd_spaces_raises_exit(test_input):
    generator = read_input_tree(test_input)
    assert next(generator) == TreeData(1, 0, True, 'src', '')
    try:
        next(generator)
        assert False
    except SystemExit as e:
        assert True
