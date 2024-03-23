"""Testing File Validation Methods.
"""
from input.tree_data import TreeData
import pytest
from pathlib import Path

from input.data_directory import DataDirectory
from input.file_validation import validate_input_file, validate_directory, get_file_extension


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
def test_validate_trim_data_file_does_not_yet_exist_returns_data(test_input, expect):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        #
        c.setattr(Path, 'glob', lambda _, x: iter([]))
        assert data_dir.validate_trim(test_input) == expect


def test_validate_trim_empty_data_label_returns_none():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        #
        test_input = TreeData(1, 0, False, "file_name", '')
        assert data_dir.validate_trim(test_input) is None


def test_validate_trim_input_is_dir_returns_none():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        #
        c.setattr(Path, 'glob', yield_path)
        test_input = TreeData(1, 0, True, "file_name", data_label)
        assert data_dir.validate_trim(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    [
        (TreeData(1, 0, False, "file_name", data_label)),
        (TreeData(1, 0, False, "file_name", data_label)),
    ]
)
def test_validate_trim_data_file_already_exists_raises_exit(test_input):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        #
        c.setattr(Path, 'glob', yield_path)
        try:
            data_dir.validate_trim(test_input)
            assert False
        except SystemExit as e:
            assert True
