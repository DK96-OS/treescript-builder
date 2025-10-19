""" The Modes of Control applied during the program operation.
"""
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import override


class ControlMode(ABC):
    """ An empty abstract class used in type hints.
 - Intended to be extended by the dataclasses in this module.
    """


@dataclass(frozen=True)
class WriteControlModes(ControlMode):
    """ The set of Controls for a Write operation.
    """
    validate: bool = True
    overwrite: bool = False
    continue_build: bool = False
    exact_build: bool = False


@dataclass(frozen=True)
class TextMergeControlModes(ControlMode):
    """ The set of Controls for a Text Merge.
    """
    prepend_merge: bool = False
    continue_build: bool = False
