"""Tree Building Operations
"""
from pathlib import Path
from typing import Optional

from input.input_data import InputData
from tree.tree_worker import TreeWorker


def build(input_data: InputData):
    worker = TreeWorker(input_data.data_dir)
    for data in input_data.get_tree_data():
        if not worker.build(data):
            exit("Failed Operation: name=" + data.name + ", depth=" + data.depth)


def create_file(
    path: Path,
    data: Optional[str]
) -> bool:
    """Ensure that a File at the given path exists.
    If the Data String is provided, 

    Parameters:
    - path (Path): The Path to the File to be created, and written to.
    - data (str, optional): The Data to be written to the File Content.

    Returns:
    bool - Whether the File operation succeeded.
    """
    with open(path, 'w') as f:
        if data is None or data == "":
            return True
        f.write(data)
    return True


def make_dir_exist(
    path: Path
):
    """Ensure that the Directory at the given Path exists.
    """
    if path.exists():
        return
    path.mkdir(exist_ok=True)
