"""Tree Building Operations
"""
from pathlib import Path

from tree.instruction_data import InstructionData


def build(instructions: tuple[InstructionData]):
    """
    Execute the Instructions in build mode.

    Parameters:
    - instructions(tuple[InstructionData]): The Instructions to execute. 
    
    Returns:
    tuple[bool] - The success or failure of each instruction.
    """
    return (_build(i) for i in instructions)


def _build(i: InstructionData) -> bool:
    """
    Execute a single instruction.

    Parameters:
    - instruction(InstructionData): The data required to execute the operation.
    
    Returns:
    bool - Whether the given operation succeeded.
    """
    if i.is_dir:
        return _make_dir_exist(i.path)
    elif i.data_path is None:
        i.path.touch()
        return True
    else:
        return _create_file(i.path, i.data_path)


def _create_file(
    path: Path,
    data: Path
) -> bool:
    """
    Create a File at the given path, with data from the Data Directory.

    Parameters:
    - path (Path): The Path to the File to be created, and written to.
    - data (Path): A Data Directory Path to be copied to the new File.

    Returns:
    bool - Whether the File operation succeeded.
    """
    from input.file_validation import read_file
    data_str = read_file(data)
    if data_str is None or data_str == '':
        path.touch()
    else:
        path.write_text(data_str)
    return True


def _make_dir_exist(
    path: Path
) -> bool:
    """
    Ensure that the Directory at the given Path exists.

    Parameters:
    - path (Path): The Path to the File to be created, and written to.
   
    """
    if path.exists():
        return True
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except:
        return False
