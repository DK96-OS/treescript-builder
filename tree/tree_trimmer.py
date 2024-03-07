"""Tree Trimming Methods.
"""
from pathlib import Path

from input.input_data import InputData
from tree.tree_worker import TreeWorker


def trim(input_data: InputData):
    """
    """
    worker = TreeWorker(input_data.data_dir)
    for data in input_data.get_tree_data():
        if not worker.remove(data):
            exit("Failed Operation: name=" + data.name + ", depth=" + data.depth)
    worker.cleanup_path_stack()


def remove_file(
    path: Path
):
    """
    Remove a File from the Tree.
    Moves the File if Data Directory and Data Label are given.
    
    Parameters:
    - path (Path): The path to the File.
    - data_dir (Path, optional): The Data Directory Path.
    - data_label (str, optional): The Label for the Data Contents of the File being removed.
    """
    path.unlink(missing_ok=True)


def remove_dir(
    path: Path,
) -> bool:
    """Tries to Remove a Directory if it is Empty.

    Parameters:
    - path (Path): The path to the Directory.

    Returns:
    bool : Whether the Directory was Empty and has been removed.
    """
    # Check if it is empty
    if len(path.glob('*')) > 0:
        return False
    path.rmdir()
    return True
