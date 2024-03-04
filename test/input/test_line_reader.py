import pytest
from input.line_reader import _calculate_depth, _process_line
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
    try:
        _calculate_depth(test_input)
        assert False
    except ValueError as e:
        assert True


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
def test_calculate_depth_dir_odd_spaces_raises_exit(test_input):
    try:
        _calculate_depth(test_input)
        assert False
    except ValueError as e:
        assert True


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + 'file', TreeData(depth, False, 'file', ''))
        for depth in range(0, 4)
    ]
)
def test_process_line_file_returns_data(test_input, expect):
    assert _process_line(test_input) == expect


@pytest.mark.parametrize(
    "test_input", 
    [
        (create_depth(depth) + ' ' + 'file')
        for depth in range(0, 4)
    ]
)
def test_process_line_file_odd_spaces_raises_exit(test_input):
    try:
        _process_line(test_input)
        assert False
    except ValueError as e:
        assert True


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + 'file DataLabel', TreeData(depth, False, 'file', 'DataLabel'))
        for depth in range(0, 4)
    ]
)
def test_process_line_file_data_label_returns_data(test_input, expect):
    assert _process_line(test_input) == expect


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + 'file ', TreeData(depth, False, 'file', ''))
        for depth in range(0, 4)
    ]
)
def test_process_line_file_trailing_space_returns_data(test_input, expect):
    assert _process_line(test_input) == expect


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (create_depth(depth) + dir, TreeData(depth, True, dir.strip('/\\'), ''))
        for dir in dir_variants
        for depth in range(0, 4)
    ]
)
def test_process_line_dir_returns_data(test_input, expect):
    assert _process_line(test_input) == expect


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
        _process_line(test_input)
        assert False
    except ValueError as e:
        assert True


#todo: More Process Line Coverage
#todo: Test Read Input Tree

