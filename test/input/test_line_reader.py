import unittest
from input.line_reader import _calculate_depth, process_line
from data.instruction_data import InstructionData


class TestLineReader(unittest.TestCase):

    def setUp(self):
        """ Create Data Structures For Tests
        Directory Variants (dir_variants) : 
            A tuple of all possible ways that a directory may be represented.
        """
        self.dir_variants = ('/dir', 'dir/', '\\dir', 'dir\\')

    def test_create_depth_space(self):
        for depth in range(0, 15):
            str_len = len(create_depth(depth, 0))
            self.assertEqual(str_len, 2 * depth)

    def test_calculate_depth_file(self):
        for depth in range(0, 15):
            self.assertEqual(_calculate_depth(create_depth(depth, 0) + 'file'), depth)

    def test_create_depth_space_char_3(self):
        for depth in range(0, 15):
            self.assertEqual(_calculate_depth(create_depth(depth, 3) + 'file'), depth)

    def test_calculate_depth_dir_variants(self):
        for var in self.dir_variants:
            for depth in range(0, 15):
                input_line = create_depth(depth, 3) + var
                self.assertEqual(
                    _calculate_depth(input_line), depth
                )
    
    def test_process_line_file_(self):
        file_name = 'file'
        for depth in range(3):
            input_line = create_depth(depth, 3) + file_name
            self.assertEqual(
                process_line(input_line),
                InstructionData(depth, False, file_name, "")
            )
    
    def test_process_line_dir_(self):
        for dir_path in self.dir_variants:
            for depth in range(15):
                input_line = create_depth(depth, 3) + dir_path
                dir_name = dir_path.strip('/\\')
                self.assertEqual(
                    process_line(input_line),
                    InstructionData(depth, True, dir_name, "")
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

SPACE_CHARS = (' ', ' ', ' ', ' ')


def create_depth(depth: int, space_char: int = 0) -> str:
    """Creates a string of space chars equivalent to the given depth.

	Parameters:
	- depth (int): The amount of depth in the Tree Node Structure.
	- space_char (int): The specific whitespace character to use. Default is the first.

	Returns:
	str: The Strings for each Space Char, of a given depth length.
	"""
    char = SPACE_CHARS[0]
    if 0 < space_char < len(SPACE_CHARS):
        char = SPACE_CHARS[space_char]
    # Default
    return char * depth * 2
