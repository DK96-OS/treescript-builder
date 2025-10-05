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
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        test_input = TreeData(1, 0, False, "file_name", '')
        assert DataDirectory(ftb_path).validate_trim(test_input) is None


def test_validate_trim_datadir_does_not_exist_raises_exit():
    # Ignore IsDir
    test_input = TreeData(1, 0, True, "file_name", data_label)
    with pytest.MonkeyPatch().context() as c:
        # The DataDir exists
        c.setattr(Path, 'exists', lambda _: False)
        with pytest.raises(SystemExit):
            DataDirectory(ftb_path).validate_trim(test_input)


def test_validate_trim_isdir_does_not_exist_returns_path():
    # Ignore IsDir
    test_input = TreeData(1, 0, True, "file_name", data_label)
    with pytest.MonkeyPatch().context() as c:
        # The DataDir exists
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        # DataFile does not exist
        c.setattr(Path, 'exists', lambda _: True)
        assert data_dir.validate_trim(test_input) == ftb_path / data_label


@pytest.mark.parametrize(
    "test_input",
    [
        (TreeData(1, 0, False, "file_name", data_label)),
        (TreeData(2, 1, False, "f2", data_label)),
    ]
)
def test_validate_trim_data_file_already_exists_raises_exit(test_input):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'glob', yield_path)
        with pytest.raises(SystemExit):
            DataDirectory(ftb_path).validate_trim(test_input)
