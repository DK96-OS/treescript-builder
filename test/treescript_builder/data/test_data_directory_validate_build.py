""" Testing File Validation Methods.
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
def test_validate_build_input_file_returns_data(test_input, expect):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True) # The DataDir Exists
        c.setattr(Path, 'glob', yield_path)
        assert DataDirectory(ftb_path).validate_build(test_input) == expect


def test_validate_build_empty_data_label_returns_none():
    test_input = TreeData(1, 0, False, "file_name", '')
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True) # The DataDir Exists
        c.setattr(Path, 'glob', yield_path)
        assert DataDirectory(ftb_path).validate_build(test_input) is None


def test_validate_build_isdir_plus_empty_data_label_returns_none():
    # Ignores the IsDir attribute
    test_input = TreeData(1, 0, True, "file_name", '')
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True) # The DataDir Exists
        c.setattr(Path, 'glob', yield_path)
        # Empty DataLabel should return None for compatibility with 0.1.x
        assert DataDirectory(ftb_path).validate_build(test_input) is None


def test_validate_build_isdir_returns_path_anyway():
    test_input = TreeData(1, 0, True, "file_name", data_label)
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True) # The DataDir Exists
        c.setattr(Path, 'glob', yield_path)
        assert DataDirectory(ftb_path).validate_build(test_input) == ftb_path / data_label


@pytest.mark.parametrize(
    "test_input",
    [
        (TreeData(1, 0, False, "file&", data_label)),
        (TreeData(1, 0, False, "#file", data_label)),
        (TreeData(1, 0, False, "!file", data_label)),
    ]
)
def test_validate_build_invalid_filename_raises_exit(test_input):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True) # The DataDir Exists
        with pytest.raises(SystemExit):
            DataDirectory(ftb_path).validate_build(test_input)


@pytest.mark.parametrize(
    "test_input",
    [
        (TreeData(1, 0, False, "file", "any/")),
        (TreeData(1, 0, False, "file", "/any")),
        (TreeData(1, 0, False, "file", "a/ny")),
        (TreeData(1, 0, False, "file", "/")),
        (TreeData(1, 0, False, "file", ".")),
        (TreeData(1, 0, False, "file", "..")),
        (TreeData(1, 0, False, "file", "../")),
        (TreeData(1, 0, False, "file", "/..")),
        (TreeData(1, 0, False, "file", "/../")),
        (TreeData(1, 0, False, "file", "~")),
        (TreeData(1, 0, False, "file", "@")),
        (TreeData(1, 0, False, "file", "%")),
        (TreeData(1, 0, False, "file", "$")),
        (TreeData(1, 0, False, "file", "#")),
    ]
)
def test_validate_build_invalid_datalabel_raises_exit(test_input):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        with pytest.raises(SystemExit):
            DataDirectory(ftb_path).validate_build(test_input)
