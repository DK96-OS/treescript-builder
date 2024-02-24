"""
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProceduralData:
    """ A piece of Data to be used in a procedural algorithm.
    Attributes:
    - depth (int): The depth in the file tree for this operation.
    - is_dir (bool): Whether the operation acts on a directory.
    - name (str): The Name of the File Tree Node.
    - data_arg (str): The Data Argument to apply.
    """
    
    depth: int
    is_dir: bool
    name: str
    data_arg: str
