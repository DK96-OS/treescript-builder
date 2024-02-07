"""File Operations
"""
from pathlib import Path
from typing import Optional


def create_file(
    path: Path,
    data: Optional[str]
) -> bool:
    """Ensure that a File at the given path exists.
    If the Data String is provided, 

    Parameters:
    - path (Path): The Path to the File to be created, and written to.
    - data (str, optional): The Data to be written to the File Content.
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
    if dir.exists():
        return
    dir.mkdir()


def remove_file(
    path: Path,
    data_dir: Optional[Path] = None,
    data_label: Optional[str] = None
):
    """Remove a File from the Tree.
    Moves the File if Data Directory and Data Label are given.
    
    Parameters:
    - path (Path): The path to the File.
    - data_dir (Path, optional): The Data Directory Path.
    - data_label (str, optional): The Label for the Data Contents of the File being removed.
    """
    if data_dir is None or data_label is None:
        path.unlink()
    else:
        # todo:
        path.rename(str(path), data_dir + data_label)


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
    if len(path.glob('*')) == 0:
        path.rmdir()
        return True
    return False
