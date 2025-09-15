""" Validation Methods for Program Option Arguments.
 Author: DK96-OS 2025
"""
from treescript_builder.data.control_modes import ControlMode, TextMergeControlModes, WriteControlModes
from treescript_builder.input.argument_data import ArgumentData


def get_control_modes_from_arg_data(
    arg_data: ArgumentData,
) -> ControlMode:
    """ Determine the ControlMode data structure to use for the given ArgumentData instance.

**Parameters:**
 - arg_data (ArgumentData): The argument dataclass to obtain ControlMode information from. 

**Returns:**
 ControlMode - The ControlMode dataclass, either a TextMergeControlModes or WriteControlModes instance, see control_modes module for implementations.
    """
    return TextMergeControlModes(
        prepend_merge=arg_data.text_prepend,
        continue_build=arg_data.control_continue,
    ) if (arg_data.text_prepend or arg_data.text_append) else\
        WriteControlModes(
            validate=arg_data.control_validate,
            overwrite=arg_data.control_overwrite,
            continue_build=arg_data.control_continue,
            exact_build=arg_data.control_exact_build,
        )


def get_verbosity_from_args(
    control_mode: ControlMode,
    verbosity: int,
) -> int:
    """ Compare given verbosity and Control Modes to determine the appropriate verbosity..

**Parameters:**
 - control_mode (ControlMode): The dataclass containing the ControlModes.
 - verbosity (int): The verbosity level given in the ArgumentData.

**Minimum Verbosity Level 1:**
The following ControlModes have an increased risk, and are assigned a minimum verbosity of 1.
 - ControlMode.OVERWRITE
 - ControlMode.CONTINUE
 - TextMode.APPEND
 - TextMode.PREPEND

**Returns:**
 int - An improved verbosity parameter, considering the given ControlModes.
    """
    if verbosity > 0:
        if verbosity > 2:
            raise ValueError
        return verbosity
    if isinstance(control_mode, TextMergeControlModes):
        return 1
    elif isinstance(control_mode, WriteControlModes):
        if control_mode.overwrite or control_mode.continue_build:
            return 1
    else:
        raise TypeError
    return 0
