""" The Modes of Control applied during the program operation.
"""
from abc import abstractmethod
from dataclasses import dataclass
from typing import override


class ControlMode:
    """ An empty abstract class used in type hints.
 - Intended to be extended by the dataclasses in this module.
    """
    @abstractmethod
    def get_verbose_overview(self, verbosity: int) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class WriteControlModes(ControlMode):
    """ The set of Controls for a Write operation.
    """
    validate: bool = True
    overwrite: bool = False
    continue_build: bool = False
    exact_build: bool = False
    
    @override
    def get_verbose_overview(self, verbosity: int) -> str:
        if verbosity < 2:
            return ""
        if self.overwrite:
            if self.continue_build:
                return "OVERWRITE, CONTINUE:"
            return "OVERWRITE"
        if self.continue_build:
            return "WRITE, CONTINUE:"
        return "WRITE"


@dataclass(frozen=True)
class TextMergeControlModes(ControlMode):
    """ The set of Controls for a Text Merge.
    """
    prepend_merge: bool = False
    continue_build: bool = False

    @override
    def get_verbose_overview(self, verbosity: int) -> str:
        if verbosity < 2:
            return ""
        if self.prepend_merge:
            return "PREPEND:"
        return "APPEND:"
