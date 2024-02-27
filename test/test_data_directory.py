import unittest
from src.data_directory import get_file_extension, is_valid_data_label, DataDirectory


class TestDataDirectory(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_file_extension_empty_str_returns_none(self):
        self.assertIsNone(
            get_file_extension("")
        )

    def test_get_file_extension_space_char_returns_none(self):
        self.assertIsNone(
            get_file_extension(" ")
        )
    
    def test_get_file_extension_name_only_returns_none(self):
        self.assertIsNone(
            get_file_extension("name")
        )
    
    def test_get_file_extension_java_file_returns_java(self):
        self.assertEqual(
            "java",
            get_file_extension("ClassName.java")
        )
    
    def test_get_file_extension_python_file_returns_py(self):
        self.assertEqual(
            "py",
            get_file_extension("python_script.py")
        )
    
    def test_is_valid_data_label_empty_str_returns_false(self):
        self.assertFalse(
            is_valid_data_label("")
        )
    
    def test_is_valid_data_label_space_char_returns_false(self):
        self.assertFalse(
            is_valid_data_label(" ")
        )
    
    def test_is_valid_data_label_name_returns_true(self):
        self.assertTrue(
            is_valid_data_label("Name")
        )
    
    def test_is_valid_data_label_file_with_ext_returns_true(self):
        self.assertTrue(
            is_valid_data_label("ClassName.java")
        )
    
    def test_is_valid_data_label_file_with_numbers_returns_true(self):
        self.assertTrue(
            is_valid_data_label("FileNumber23")
        )
    
    def test_is_valid_data_label_file_with_number_and_ext_returns_true(self):
        self.assertTrue(
            is_valid_data_label("FileNumber23.txt")
        )
