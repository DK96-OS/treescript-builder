import unittest
import pytest
from input.line_reader import _calculate_depth, _process_line
from input.tree_data import TreeData
from test.input import create_depth


@pytest.mark.parametrize(
    "test_input,expect", 
    [ 
        (create_depth(depth) + 'file', depth)
        for depth in range(0, 9)
    ]
)
def test_calculate_depth_file_returns_true(test_input, expect):
    assert _calculate_depth(test_input) == expect

# Directory Variants: A tuple of all possible ways that a directory may be represented.
dir_variants = ('/dir', 'dir/', '\\dir', 'dir\\')

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


class TestLineReader(unittest.TestCase):

    def setUp(self):
        """ Create Data Structures For Tests
        Directory Variants (dir_variants) : 
            A tuple of all possible ways that a directory may be represented.
        """
        self.dir_variants = ('/dir', 'dir/', '\\dir', 'dir\\')

    def test_calculate_depth_file(self):
        for depth in range(0, 15):
            self.assertEqual(_calculate_depth(create_depth(depth) + 'file'), depth)

    def test_create_depth_space_char_3(self):
        for depth in range(0, 15):
            self.assertEqual(_calculate_depth(create_depth(depth) + 'file'), depth)

    def test_calculate_depth_dir_variants(self):
        for var in self.dir_variants:
            for depth in range(0, 15):
                input_line = create_depth(depth) + var
                self.assertEqual(
                    _calculate_depth(input_line), depth
                )
    
    def test_process_line_file_(self):
        file_name = 'file'
        for depth in range(3):
            input_line = create_depth(depth) + file_name
            self.assertEqual(
                _process_line(input_line),
                TreeData(depth, False, file_name, "")
            )
    
    def test_process_line_dir_(self):
        for dir_path in self.dir_variants:
            for depth in range(15):
                input_line = create_depth(depth) + dir_path
                dir_name = dir_path.strip('/\\')
                self.assertEqual(
                    _process_line(input_line),
                    TreeData(depth, True, dir_name, "")
                )

    def test_depth_0_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(_calculate_depth(var), 0)

    def test_depth_1_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(_calculate_depth("  " + var), 1)

    def test_depth_1_file(self):
        self.assertEqual(_calculate_depth("  file1"), 1)

    def test_depth_2_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(_calculate_depth("    " + var), 2)

    def test_depth_2_file(self):
        self.assertEqual(_calculate_depth("    file2"), 2)

    def test_depth_3_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(_calculate_depth("      " + var), 3)

    def test_depth_3_file(self):
        self.assertEqual(_calculate_depth("      file3"), 3)


if __name__ == '__main__':
    unittest.main()
