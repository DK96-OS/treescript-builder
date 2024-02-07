import unittest
from input_line_reader import create_depth, calculate_depth, process_line
from procedural_data import ProceduralData


class TestInputLineReader(unittest.TestCase):

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
            self.assertEqual(calculate_depth(create_depth(depth, 0) + 'file'), depth)

    def test_create_depth_space_char_3(self):
        for depth in range(0, 15):
            self.assertEqual(calculate_depth(create_depth(depth, 3) + 'file'), depth)

    def test_calculate_depth_dir_variants(self):
        for var in self.dir_variants:
            for depth in range(0, 15):
                input_line = create_depth(depth, 3) + var
                self.assertEqual(
                    calculate_depth(input_line), depth
                )
    
    def test_process_line_file_(self):
        file_name = 'file'
        for depth in range(3):
            input_line = create_depth(depth, 3) + file_name
            self.assertEqual(
                process_line(input_line),
                ProceduralData(depth, False, file_name, "")
            )
    
    def test_process_line_dir_(self):
        for dir_path in self.dir_variants:
            for depth in range(15):
                input_line = create_depth(depth, 3) + dir_path
                dir_name = dir_path.strip('/\\')
                self.assertEqual(
                    process_line(input_line),
                    ProceduralData(depth, True, dir_name, "")
                )

    def test_depth_0_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(calculate_depth(var), 0)

    def test_depth_1_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(calculate_depth("  " + var), 1)

    def test_depth_1_file(self):
        self.assertEqual(calculate_depth("  file1"), 1)

    def test_depth_2_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(calculate_depth("    " + var), 2)

    def test_depth_2_file(self):
        self.assertEqual(calculate_depth("    file2"), 2)

    def test_depth_3_dir_variants(self):
        for var in self.dir_variants:
            self.assertEqual(calculate_depth("      " + var), 3)

    def test_depth_3_file(self):
        self.assertEqual(calculate_depth("      file3"), 3)


if __name__ == '__main__':
    unittest.main()
