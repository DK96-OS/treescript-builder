"""Testing Data Directory
"""
from pathlib import Path

import pytest

from treescript_builder.tree.data_directory import DataDirectory


@pytest.mark.parametrize(
    "test_input",
    [
        'data_dir',
        None,
    ]
)
def test_data_directory_init_non_path_raise_exit(test_input):
    with pytest.raises(SystemExit):
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