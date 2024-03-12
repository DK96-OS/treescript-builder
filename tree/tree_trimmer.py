"""Tree Trimming Methods.
"""
from pathlib import Path

from tree.instruction_data import InstructionData


def trim(instructions: tuple[InstructionData, ...]) -> tuple[bool, ...]:
    """
    Execute the Instructions in trim mode.

    Parameters:
    - instructions(tuple[InstructionData]): The Instructions to execute. 
    
    Returns:
    tuple[bool] - The success or failure of each instruction.
    """
    return tuple(_trim(i) for i in instructions)


def _trim(instruct: InstructionData) -> bool:
    if instruct.is_dir:
        return _remove_dir(instruct.path)
    elif instruct.data_path is None:
        try:
            instruct.path.unlink(missing_ok=True)
            return True
        except:
            return False
    else:
        return _extract_file(instruct.path, instruct.data_path)


def _extract_file(
    path: Path,
    data: Path
) -> bool:
    """
    Moves the File to the Data Directory.
    
    Parameters:
    - path (Path): The path to the File in the Tree.
    - data (Path): A Path to a File in the Data Directory.

    Returns:
    bool - Whether the entire operation succeeded.
    """
    from input.file_validation import read_file
    try:
        data_str = read_file(path)
        if data_str is None or len(data_str) == 0:
            data.touch()
        else:
            data.write_text(data_str)
        path.unlink()
    except:
        return False
    return True


def _remove_dir(
    path: Path,
) -> bool:
    """
    Tries to Remove a Directory, if it is Empty.

    Parameters:
    - path (Path): The path to the Directory.

    Returns:
    bool : Whether the Directory was Empty, and has been removed.
    """
    try:
        path.rmdir()
    except:
        # Was not empty
        return False
    return True
