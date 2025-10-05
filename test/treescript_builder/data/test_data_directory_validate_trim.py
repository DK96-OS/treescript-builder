"""Testing File Validation Methods.
"""
from pathlib import Path

import pytest

from treescript_builder.data.data_directory import DataDirectory
from treescript_builder.data.tree_data import TreeData

ftb_path = Path('.ftb/')
data_label = 'data_label'


def yield_path(_, x):
    """Generator used to mock the Path object glob method."""
    yield ftb_path / data_label


@pytest.mark.parametrize(
    "test_input,expect",
    [
        (TreeData(1, 0, False, "file_name", 'data_label'), ftb_path / data_label),
        (TreeData(1, 0, False, "file_name", 'data_label'), ftb_path / data_label),
    ]
)
def test_validate_trim_data_file_does_not_yet_exist_returns_path(test_input, expect):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'glob', lambda _, x: iter([]))
        assert DataDirectory(ftb_path).validate_trim(test_input) == expect


def test_validate_trim_empty_data_label_returns_none():
    test_input = TreeData(1, 0, False, "file_name", '')
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        assert DataDirectory(ftb_path).validate_trim(test_input) is None


def test_validate_trim_datadir_does_not_exist_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False) # The DataDir does not exist!
        with pytest.raises(SystemExit, match='The Data Directory must be a Path that Exists!'):
            DataDirectory(ftb_path)


def test_validate_trim_isdir_does_not_exist_returns_path():
    test_input = TreeData(1, 0, True, "file_name", data_label) # Ignore IsDir
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True) # The DataDir exists
        assert DataDirectory(ftb_path).validate_trim(test_input) == ftb_path / data_label


@pytest.mark.parametrize(
    "test_input",
    [
        (TreeData(1, 0, False, "file_name", data_label)),
        (TreeData(2, 1, False, "f2", data_label)),
    ]
)
def test_validate_trim_data_file_already_exists_raises_exit(test_input):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True) # The DataDir exists.
        c.setattr(Path, 'glob', yield_path) # The DataFile exists.
        with pytest.raises(SystemExit, match='Data File already exists!'):
            DataDirectory(ftb_path).validate_trim(test_input)


def test_validate_trim_duplicate_data_labels_raises_exit():
    test_input1 = TreeData(1, 0, False, "f1", data_label)
    test_input2 = TreeData(2, 0, False, "f2", '')
    test_input3 = TreeData(3, 0, False, "f3", data_label)
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        # First 2 Inputs are valid
        assert data_dir.validate_trim(test_input1) == ftb_path / data_label
        assert data_dir.validate_trim(test_input2) is None # No DataLabel here. Compatible with 0.1.x
        # The next is a duplicate DataLabel!
        with pytest.raises(SystemExit, match='Duplicate DataLabels in Trim Operation on Line: 3'):
            data_dir.validate_trim(test_input3)
