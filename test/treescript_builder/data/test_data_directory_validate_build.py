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
def test_validate_build_input_file_returns_data(test_input, expect):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        #
        c.setattr(Path, 'glob', yield_path)
        assert data_dir.validate_build(test_input) == expect


@pytest.mark.parametrize(
    "test_input",
    [
        (TreeData(1, 0, False, "file_name", '')),
        (TreeData(1, 0, True, "file_name", data_label)),
    ]
)
def test_validate_build_invalid_tree_data_returns_none(test_input):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        #
        c.setattr(Path, 'glob', yield_path)
        assert data_dir.validate_build(test_input) is None


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
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        with pytest.raises(SystemExit):
            data_dir.validate_build(test_input)


@pytest.mark.parametrize(
    "test_input",
    [
        (TreeData(1, 0, False, "file", "any/")),
        (TreeData(1, 0, False, "file", "/any")),
        (TreeData(1, 0, False, "file", "a/ny")),
        (TreeData(1, 0, False, "file", "/")),
        (TreeData(1, 0, False, "file", "@")),
        (TreeData(1, 0, False, "file", "%")),
        (TreeData(1, 0, False, "file", "$")),
        (TreeData(1, 0, False, "file", "#")),
    ]
)
def test_validate_build_invalid_datalabel_raises_exit(test_input):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = DataDirectory(ftb_path)
        with pytest.raises(SystemExit):
            data_dir.validate_build(test_input)
