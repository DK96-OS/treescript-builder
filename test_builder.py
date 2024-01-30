import unittest
from builder import join_path_stack
from input_line_reader import process_line


class TestBuilder(unittest.TestCase):

    def test_join_path_stack_2(self):
        input_stack = ['a', 'b', ]
        expected_length = 2 + 1 # one for each node, plus 1 separator
        output = join_path_stack(input_stack)
        print(output)
        self.assertEqual(
            len(output),
            expected_length
        )
    
    def test_join_path_stack_4(self):
        input_stack = ['a', 'b', 'c', 'd']
        expected_length = 4 + 3 # one for each node, plus 3 separators
        self.assertEqual(
            len(join_path_stack(input_stack)),
            expected_length
        )
    
    def test_process_line_file(self):
        self.assertEqual(process_line("file1"), (False, 'file1'))

    def test_process_line_file_level_2(self):
        self.assertEqual(process_line("    file1"), (False, 'file1'))

    def test_process_line_directory_level_0_slash_first(self):
        self.assertEqual(process_line("/dir1"), (True, 'dir1'))

    def test_process_line_directory_level_1_slash_first(self):
        self.assertEqual(process_line("  /dir1"), (True, 'dir1'))

    def test_process_line_directory_level_0_slash_last(self):
        self.assertEqual(process_line("dir1/"), (True, 'dir1'))

    def test_process_line_directory_level_1_slash_last(self):
        self.assertEqual(process_line("  dir1/"), (True, 'dir1'))

    def test_process_line_directory_level_0_backslash_first(self):
        self.assertEqual(process_line("\\dir1"), (True, 'dir1'))

    def test_process_line_directory_level_1_backslash_first(self):
        self.assertEqual(process_line("  \\dir1"), (True, 'dir1'))

    def test_process_line_directory_level_0_backslash_last(self):
        self.assertEqual(process_line("dir1\\"), (True, 'dir1'))

    def test_process_line_directory_level_1_backslash_last(self):
        self.assertEqual(process_line("  dir1\\"), (True, 'dir1'))


if __name__ == '__main__':
    unittest.main()
