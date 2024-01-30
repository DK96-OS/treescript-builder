import unittest
from builder import join_path_stack


class TestBuilder(unittest.TestCase):

    def test_join_path_stack_2(self):
        input_stack = ['a', 'b']
        expected_length = 2 + 2 # one for each node, plus 1 separator each
        output = join_path_stack(input_stack)
        print(output)
        self.assertEqual(
            len(output),
            expected_length
        )
    
    def test_join_path_stack_4(self):
        input_stack = ['aa', 'bb', 'cc', 'dd']
        expected_length = 2 * 4 + 4 # two for each node, plus 1 separator each
        self.assertEqual(
            len(join_path_stack(input_stack)),
            expected_length
        )


if __name__ == '__main__':
    unittest.main()
