""" File Tree Worker.
"""
from typing import Optional
from pathlib import Path
from .path_stack import PathStack
from input.tree_data import TreeData
from .file_operations import create_file, make_dir_exist, read_file, remove_dir, remove_file
from data.data_directory import DataDirectory


class TreeWorker:
    """File Tree Worker.
    A Stateful Procedural Machine that executes file operations on given input data.
    """

    def __init__(self, data_dir: Optional[DataDirectory]) -> None:
        # The Path Stack during Stateful Procedural Operation
        self._path_stack = PathStack()
        # The Data Directory
        self._data_dir = data_dir

    def _search_data_dir(self, data: TreeData) -> Optional[Path]:
        """
        Search the Data Directory for a Data Label match.
        """
        # No Data Directory
        if self._data_dir is None:
            return None
        # No Data Argument
        if data.data_label == "":
            # Use the File Name
            path = self._data_dir.search_name(data.name)
            if path is None or not path.exists():
                return None
            return path
        # Search in Data Directory
        data_path = self._data_dir.search_label(
            file_name=data.name,
            data_label=data.data_label
        )
        if data_path is None:
            raise SystemError("Failed to Find Data: "+ data.data_label)
        return data_path

    def build(self, data: TreeData) -> bool:
        """
        Execute a Procedural Builder Operation.
        """
        success = self._path_stack.reduce_depth(data.depth)
        if not success:
            return False
        # Check Is Directory
        if data.is_dir:
            self._path_stack.push(data.name)
            make_dir_exist(Path(self._path_stack.join_stack()))
            return True
        # Is a File
        file_path = self._path_stack.create_path(data.name)
        # Try to Get Data
        data_path = self._search_data_dir(data)
        if data_path is None:
            return create_file(file_path)
        # Search in Data
        try:
            return create_file(file_path, read_file(data_path))
        except:
            raise SystemError("Failed File Operation")
    
    def remove(self, data: TreeData) -> bool:
        """
        Execute a Procedural Remove Operation.
        """
        # Adjust Path Stack to current Depth.
        while self._path_stack.get_depth() > data.depth:
            # Pop a Directory, get it's Path
            remove_dir(self._path_stack.create_path(self._path_stack.pop()))
        # Check Is Directory
        if data.is_dir:
            self._path_stack.append(data.name)
            return True
        # Is a File
        file_path = self._path_stack.create_path(data.name)
        # No Data Directory
        if self._data_dir is None:
            remove_file(
                self._path_stack.create_path(data.name)
            )
        # 
        self._data_dir, data.data_label
        #
        remove_file(
            self._path_stack.create_path(data.name)
        )
        return True

    def cleanup_path_stack(self):
        """
        Clears the Remaining Path Stack.
        Removes any Empty Directories Left on the Stack.
        """
        while self._path_stack.get_depth() > 0:
            # Pop a Directory, get it's Path
            dir = self._path_stack.create_path(self._path_stack.pop())
            if not remove_dir(dir):
                break
