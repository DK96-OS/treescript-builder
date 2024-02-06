""" Test Cases for Path Stack class
"""
import unittest

from pathstack import PathStack


class TestPathStack(unittest.TestCase):
    """ Test Cases
    Setup:
    - Instantiates a new PathStack, stores instance
    """

    def setUp(self):
        self.instance = PathStack()

    def test_join_stack_initial_condition(self):
        self.assertEqual(
            "./",
            self.instance.join_stack()
        )

    def test_join_stack_after_push_once(self):
        dir_name = "source"
        self.instance.push(dir_name)
        self.assertEqual(
            "./" + dir_name +"/",
            self.instance.join_stack()
        )

    def test_join_stack_after_push_twice(self):
        dir_name_1, dir_name_2 = "src", "main"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertEqual(
            "./" + dir_name_1 +"/" + dir_name_2 + "/",
            self.instance.join_stack()
        )

    def test_create_path_after_push_once(self):
        dir_name_1, file_name = "java", "Main.java"
        self.instance.push(dir_name_1)
        self.assertEqual(
            "./" + dir_name_1 + "/" + file_name,
            self.instance.create_path(file_name)
        )

    def test_get_depth_initial_condition(self):
        self.assertEqual(
            0, self.instance.get_depth()
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

    def test_reduce_depth_initial_condition_all_returns_false(self):
        for depth in range(0, 8):
            self.assertFalse(
                self.instance.reduce_depth(depth)
            )

    def test_reduce_depth_invalid_input_returns_false(self):
        # Check multiple negative numbers
        for depth in range(-1, -100, -20):
            self.assertFalse(
                self.instance.reduce_depth(depth)
            )

    def test_reduce_depth_add_one_returns_true(self):
        dir_name_1 = "src"
        self.instance.push(dir_name_1)
        self.assertTrue(
            self.instance.reduce_depth(0)
        )

    def test_reduce_depth_add_one_returns_false(self):
        dir_name_1 = "src"
        self.instance.push(dir_name_1)
        self.assertEqual(
            1, self.instance.get_depth()
        )
        self.assertFalse(
            self.instance.reduce_depth(1)
        )

    def test_reduce_depth_add_two_returns_true(self):
        dir_name_1, dir_name_2 = "src", "java"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertTrue(
            self.instance.reduce_depth(0)
        )
        self.assertEqual(
            0, self.instance.get_depth()
        )

    def test_reduce_depth_add_two_returns_true1(self):
        dir_name_1, dir_name_2 = "src", "java"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertTrue(
            self.instance.reduce_depth(1)
        )
        self.assertEqual(
            1, self.instance.get_depth()
        )

    def test_reduce_depth_add_two_returns_false(self):
        dir_name_1, dir_name_2 = "src", "java"
        self.instance.push(dir_name_1)
        self.instance.push(dir_name_2)
        self.assertFalse(
            self.instance.reduce_depth(2)
        )
        self.assertEqual(
            2, self.instance.get_depth()
        )


if __name__ == '__main__':
    unittest.main()
