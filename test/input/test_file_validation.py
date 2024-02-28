import unittest
from input.file_validation import validate_input_file, validate_directory, _get_input


class TestFileValidation(unittest.TestCase):

    def test_validate(self):
        #todo: Mock
        self.assertRaises(SystemError, validate_input_file)
