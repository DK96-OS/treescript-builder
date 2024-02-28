"""Testing the Init Section of Input Module.
"""
import unittest
from input import is_nonempty_str


class TestInit(unittest.TestCase):

    def test_is_nonempty_str_none_returns_false(self):
        self.assertFalse(is_nonempty_str(None))

    def test_is_nonempty_str_number_returns_false(self):
        self.assertFalse(is_nonempty_str(4))

    def test_is_nonempty_str_dict_returns_false(self):
        self.assertFalse(is_nonempty_str({}))

    def test_is_nonempty_str_list_returns_false(self):
        self.assertFalse(is_nonempty_str([]))

    def test_is_nonempty_str_empty_returns_false(self):
        self.assertFalse(is_nonempty_str(""))

    def test_is_nonempty_str_one_space_returns_false(self):
        self.assertFalse(is_nonempty_str(" "))

    def test_is_nonempty_str_number_char_returns_true(self):
        self.assertTrue(is_nonempty_str("1"))

    def test_is_nonempty_str_letter_returns_true(self):
        self.assertTrue(is_nonempty_str("a"))

    def test_is_nonempty_str_word_returns_true(self):
        self.assertTrue(is_nonempty_str("test"))
