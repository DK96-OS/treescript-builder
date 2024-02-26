import unittest
from input.argument_validation import validate_argument_syntax


class TestArgumentValidation(unittest.TestCase):

    def test_validate(self):
        self.assertRaises(SystemError, validate_argument_syntax)
