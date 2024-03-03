import unittest
from tree.tree_worker import TreeWorker
from input.tree_data import TreeData
from unittest.mock import patch, MagicMock


class TestTreeWorker(unittest.TestCase):

    def setUp(self):
        self.data_dir = None
        self.instance = TreeWorker(self.data_dir)

    @patch("file_operations.make_dir_exist")
    def test_build_initial_condition_dir(self):
        input_data = TreeData(
            0, True, "name", ""
        )
        self.instance.build(input_data)

    @patch("file_operations.remove_dir")
    def test_remove_initial_condition_dir(self):
        input_data = TreeData(
            0, True, "name", ""
        )
        self.instance.remove(input_data)

    def test_cleanup_path_stack_initial_condition_does_nothing(self):
        self.instance.cleanup_path_stack()
