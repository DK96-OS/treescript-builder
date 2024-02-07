""" File Tree Worker
"""
from typing import Optional
from pathlib import Path
from path_stack import PathStack
from procedural_data import ProceduralData
from file_operations import create_file, make_dir_exist, remove_dir, remove_file


class TreeWorker:
    """File Tree Worker"""

    def __init__(self, data_dir: Optional[Path]) -> None:
        self._data_dir = data_dir
        self._path_stack = PathStack()

    def build(self, data: ProceduralData) -> bool:
        """Execute a Procedural Builder Operation"""
        success = self._path_stack.reduce_depth(data.depth)
        if not success:
            return False
        # Split Directory and File Handling
        if data.is_dir:
            self._path_stack.push(data.name)
            make_dir_exist(Path(self._path_stack.join_stack()))
        elif self._data_dir is None:
            create_file(
                self._path_stack.create_path(data.name),
                data.data_arg
            )
        else:
            data_path = self._data_dir
            (data.data_arg)
            create_file(
                self._path_stack.create_path(data.name),
                data_path.read_text()
            )
    
    def remove(self, data: ProceduralData) -> bool:
        """Execute a Procedural Remove Operation"""
        # Adjust Path Stack to current Depth.
        while self._path_stack.get_depth() > data.depth:
            # Pop a Directory, get it's Path
            remove_dir(self._path_stack.create_path(self._path_stack.pop()))
        # Split Directory and File Handling
        if data.is_dir:
            self._path_stack.append(data.name)
        else:
            remove_file(
                self._path_stack.create_path(data.name),
                self._data_dir,
                data.data_arg
            )

    def cleanup(self):
        self._path_stack.pop()
