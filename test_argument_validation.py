import unittest
from argument_validation import ArgumentValidation


class TestArgumentValidation(unittest.TestCase):

    def setUp(self):
        self.instance = ArgumentValidation()

    def test_parse_args_no_args(self):
        self.assertFalse(
            self.instance.parse_args()
        )

    def test_parse_args_empty_args(self):
        self.assertFalse(
            self.instance.parse_args([])
        )

    def test_parse_args_single_arg(self):
        file_name = 'input_file'
        self.assertTrue(
            self.instance.parse_args([file_name])
        )
        self.assertEqual(
            file_name, self.instance.get_input().tree_file
        )

    def test_parse_args_two_args(self):
        file_name = 'tree-struct'
        data_dir = "./filedata"
        self.assertTrue(
            self.instance.parse_args([file_name, '--data_dir=' + data_dir])
        )
        self.assertEqual(
            file_name, self.instance.get_input().tree_file
        )
        self.assertEqual(
            data_dir, self.instance.get_input().data_dir
        )
