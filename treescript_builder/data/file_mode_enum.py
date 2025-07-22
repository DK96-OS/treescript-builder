""" The Available Modes of File Operations.
"""
from enum import IntEnum, auto


class FileModeEnum(IntEnum):
    """ The File Operation Mode.

**Options:**
 - APPEND (default): Add data to the end of files in the operation.
 - CANCEL: Prevent overwriting by cancelling any file operation necessary.
 - PREPEND: Insert data at the start of each file in the operation.
 - OVERWRITE: Write over all files in the operation with the data.
    """
    APPEND = auto()
    CANCEL = auto()
    PREPEND = auto()
    OVERWRITE = auto()
