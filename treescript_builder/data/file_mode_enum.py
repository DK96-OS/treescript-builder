""" The Available Modes of File Operations.
"""
from enum import IntEnum, auto


class FileModeEnum(IntEnum):
    """ The File Operation Mode.

**Options:**
 - APPEND (default): Add data to the end of files in the operation.
 - CANCEL: Prevent overwriting by cancelling any individual copy operation, without stopping the build process.
 - PREPEND: Insert data at the start of each file in the operation.
 - OVERWRITE: Write over all files in the operation with the data.
 - MOVE: Move files (rename paths) instead of copying data.
    """
    APPEND = auto()
    CANCEL = auto()
    PREPEND = auto()
    OVERWRITE = auto()
    MOVE = auto()
