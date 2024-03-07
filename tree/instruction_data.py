"""The Instruction Data in a Tree Operation
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class InstructionData:
    """
    The Data required to execute the Instruction.
    """

    is_dir: bool
    path: Path
    secondary_path: Optional[Path]
