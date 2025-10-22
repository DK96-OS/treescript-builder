"""Testing Data Directory
"""
from pathlib import Path
from re import escape

import pytest

from treescript_builder.tree.data_directory import DataDirectory
from treescript_builder.data.data_directory import DataDirectory, get_data_dir_validator
from treescript_builder.data.tree_data import TreeData


ftb_path = Path('.ftb/')
data_label = 'data_label'


def yield_path(_, x):
    """Generator used to mock the Path object glob method."""
    yield ftb_path / data_label


@pytest.mark.parametrize(
    "test_input",
    [
        'data_dir',
        None,
    ]
)
def test_data_directory_init_non_path_raise_exit(test_input):
    with pytest.raises(TypeError):
        DataDirectory(test_input)


def test_data_directory_init_dir_does_not_exist_raise_exit():
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: False)
        with pytest.raises(SystemExit):
            DataDirectory(Path('data_dir'))


@pytest.mark.parametrize(
    "test_input",
    [
        '*',
        'invalid/label',
    ]
)
def test_search_label_invalid_label_returns_none(test_input):
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: True)
        instance = DataDirectory(Path('data_dir'))
        assert instance._search_label(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    [
        'valid_label',
        'valid-label',
        'script.py',
        '123',
    ]
)
def test_search_label_does_not_exist_returns_none(test_input):
    with pytest.MonkeyPatch().context() as m:
        # When the Data Directory is created, Path must exist
        m.setattr(Path, 'exists', lambda c: True)
        instance = DataDirectory(Path('data_dir'))
        # When the Label is searched, the Path does not exist
        m.setattr(Path, 'exists', lambda c: False)
        m.setattr(Path, 'glob', lambda c, d: iter([]))
        assert instance._search_label(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    [
        'valid_label',
        'valid-label',
        'script.py',
        '123',
    ]
)
def test_search_label_exists_returns_path(test_input):
    data_dir_path = Path('data_dir')
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: True)
        instance = DataDirectory(data_dir_path)
        #
        m.setattr(Path, 'glob', lambda c, d: iter([data_dir_path / test_input]))
        assert instance._search_label(test_input) == data_dir_path / test_input


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
        with pytest.raises(SystemExit, match=escape(f'Label not found in DataDirectory on Line: {test_input.line_number}')):
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
        c.setattr(Path, 'exists', lambda _: True) # DataDir exists.
        with pytest.raises(SystemExit, match=f'Invalid Data Label on line: {test_input.line_number}'):
            DataDirectory(ftb_path).validate_build(test_input)


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
        with pytest.raises(SystemExit, match=data_directory._DATA_DIR_PATH_DOES_NOT_EXIST_MSG):
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
        with pytest.raises(SystemExit, match=data_directory._DATA_FILE_EXISTS_MSG):
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
        with pytest.raises(SystemExit, match=data_directory._DATA_LABEL_DUPLICATE_MSG):
            data_dir.validate_trim(test_input3)


@pytest.mark.parametrize(
    "tree_data", [
        TreeData(1, 0, True, "src", ''),
        TreeData(2, 1, False, "file_name.txt", ''),
    ]
)
def test_get_data_dir_validator_build_no_data_dir_tree_data_without_data_label_returns_none(tree_data):
    validator = get_data_dir_validator(None, is_trim=False)
    assert validator(tree_data) is None


@pytest.mark.parametrize(
    "tree_data", [
        TreeData(1, 0, False, "src_file", 'DataLabel'),
        TreeData(2, 1, False, "file_name.txt", '!'),
        TreeData(5, 3, False, "file_name.txt", 'file_name.txt'),
    ]
)
def test_get_data_dir_validator_build_no_data_dir_tree_data_with_data_label_raises_exit(tree_data):
    validator = get_data_dir_validator(None, is_trim=False)
    with pytest.raises(SystemExit):
        validator(tree_data)


@pytest.mark.parametrize(
    "tree_data", [
        TreeData(1, 0, True, "src", ''),
        TreeData(2, 1, False, "file_name.txt", ''),
    ]
)
def test_get_data_dir_validator_trim_no_data_dir_tree_data_without_data_label_returns_none(tree_data):
    validator = get_data_dir_validator(None, is_trim=True)
    assert validator(tree_data) is None


@pytest.mark.parametrize(
    "tree_data", [
        TreeData(1, 0, False, "src_file", 'DataLabel'),
        TreeData(2, 1, False, "file_name.txt", '!'),
        TreeData(5, 3, False, "file_name.txt", 'file_name.txt'),
    ]
)
def test_get_data_dir_validator_trim_no_data_dir_tree_data_with_data_label_raises_exit(tree_data):
    validator = get_data_dir_validator(None, is_trim=True)
    with pytest.raises(SystemExit):
        validator(tree_data)
