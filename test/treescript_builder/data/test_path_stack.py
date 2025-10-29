""" Test Cases for Path Stack class
"""
import unittest
from pathlib import Path

import pytest

from treescript_builder.data.path_stack import PathStack


class TestPathStack(unittest.TestCase):
    """ Test Cases.

**Setup:**
 - Instantiates a new PathStack, stores instance
    """

    def setUp(self):
        self.instance = PathStack()

    def test_get_depth_initial_condition_returns_zero(self):
        self.assertEqual(
            0, self.instance.get_depth()
        )

    def test_get_depth_after_push_returns_one(self):
        self.instance.push("src")
        self.assertEqual(
            1, self.instance.get_depth()
        )

    def test_pop_initial_condition_returns_none(self):
        self.assertIsNone(
            self.instance.pop()
        )

    def test_get_depth_after_push_and_pop_returns_zero(self):
        dir_name = "src"
        self.instance.push(dir_name)
        self.assertEqual(
            dir_name, self.instance.pop()
        )
        self.assertEqual(
            0, self.instance.get_depth()
        )

    def test_join_stack_initial_condition_returns_cwd(self):
        self.assertEqual(
            Path("./"),
            self.instance.join_stack()
        )

    def test_join_stack_after_push_once_returns_valid_path(self):
        dir_name = "source"
        self.instance.push(dir_name)
        self.assertEqual(
            Path("./" + dir_name +"/"),
            self.instance.join_stack()
        )

    def test_join_stack_after_push_twice_returns_valid_path(self):
        dir_name_1, dir_name_2 = "src", "main"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertEqual(
            Path("./" + dir_name_1 +"/" + dir_name_2 + "/"),
            self.instance.join_stack()
        )

    def test_get_depth_add_one(self):
        dir_name_1 = "src"
        self.instance.push(dir_name_1)
        self.assertEqual(
            1, self.instance.get_depth()
        )

    def test_get_depth_add_two(self):
        dir_name_1, dir_name_2 = "src", "java"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertEqual(
            2, self.instance.get_depth()
        )

    def test_reduce_depth_initial_condition_zero_returns_true(self):
        self.assertTrue(
            self.instance.reduce_depth(0)
        )

    def test_reduce_depth_initial_condition_above_zero_returns_false(self):
        for depth in range(1, 8):
            self.assertFalse(
                self.instance.reduce_depth(depth)
            )

    def test_reduce_depth_invalid_input_raises_index_error(self):
        # Check multiple negative numbers
        for depth in range(-1, -100, -20):
            with pytest.raises(IndexError, match='pop from empty list'):
                self.assertFalse(
                    self.instance.reduce_depth(depth)
                )

    def test_reduce_depth_add_one_depth_zero_returns_true(self):
        dir_name_1 = "src"
        self.instance.push(dir_name_1)
        self.assertTrue(
            self.instance.reduce_depth(0)
        )

    def test_reduce_depth_after_push_one_depth_zero_returns_true(self):
        dir_name_1 = "src"
        self.instance.push(dir_name_1)
        self.assertEqual(
            1, self.instance.get_depth()
        )
        self.assertTrue(
            self.instance.reduce_depth(0)
        )

    def test_reduce_depth_after_push_two_returns_true(self):
        dir_name_1, dir_name_2 = "src", "java"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertTrue(
            self.instance.reduce_depth(0)
        )
        self.assertEqual(
            0, self.instance.get_depth()
        )

    def test_reduce_depth_after_push_two_returns_true1(self):
        dir_name_1, dir_name_2 = "src", "java"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertTrue(
            self.instance.reduce_depth(1)
        )
        self.assertEqual(
            1, self.instance.get_depth()
        )

    def test_reduce_depth__two_returns_true(self):
        dir_name_1, dir_name_2 = "src", "java"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertTrue(
            self.instance.reduce_depth(2)
        )
        self.assertEqual(
            2, self.instance.get_depth()
        )


if __name__ == '__main__':
    unittest.main()