""" Testing File Validation Methods.
"""
from itertools import repeat
from pathlib import Path

import pytest

from test.treescript_builder.conftest import raise_exception
from test.treescript_builder.input.conftest import generate_filenames
from treescript_builder.input import validate_input_file, validate_directory, file_validation


class MockPathStat:
    def __init__(self, file_size: int = 400):
        self.st_mode = 2
        self.st_size = file_size


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ("file_name", "file_data"),
        ("file_name12", "12"),
        ("file_name_abcdef", '\n'.join(repeat('abcdefg', 4 * 1024))),
    ]
)
def test_validate_input_file_returns_data(test_input, expect):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: expect)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(len(expect)))
        assert validate_input_file(test_input) == expect


def test_validate_input_file_size_at_limit_returns_data():
    expected_data = 'treescript'
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: expected_data)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        assert expected_data == validate_input_file('any')


def test_validate_input_file_size_larger_than_limit_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT + 1))
        with pytest.raises(SystemExit, match=file_validation._FILE_SIZE_LIMIT_ERROR_MSG):
            validate_input_file('any')


def test_validate_input_file_does_not_exist_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        with pytest.raises(SystemExit, match=file_validation._FILE_DOES_NOT_EXIST_MSG):
            validate_input_file("file_name")


def test_validate_input_file_oserror_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: raise_exception('oserror'))
        with pytest.raises(SystemExit, match=file_validation._FILE_READ_OSERROR_MSG):
            validate_input_file("file_name")


def test_validate_input_file_ioerror_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: raise_exception('ioerror'))
        with pytest.raises(SystemExit, match=file_validation._FILE_READ_OSERROR_MSG):
            validate_input_file("file_name")


def test_validate_input_file_typeerror_raises_typerror():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: raise_exception('typeerror'))
        with pytest.raises(TypeError):
            validate_input_file("file_name")


def test_validate_input_file_valueerror_raises_valueerror():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: raise_exception('valueerror'))
        with pytest.raises(ValueError):
            validate_input_file("file_name")


def test_validate_input_file_is_empty_returns_none():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        c.setattr(Path, 'read_text', lambda _: "")
        with pytest.raises(SystemExit, match=file_validation._FILE_VALIDATION_ERROR_MSG):
            validate_input_file("file_name")


def test_validate_input_file_filenames_returns_data():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'lstat', lambda _: MockPathStat(file_validation._FILE_SIZE_LIMIT))
        for n, filename in enumerate(generate_filenames(), 1):
            expected_file_contents: str = f"{filename}{n}"
            c.setattr(Path, 'read_text', lambda _: expected_file_contents)
            assert expected_file_contents == validate_input_file(filename)


def test_validate_directory_does_not_exist_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        with pytest.raises(SystemExit):
            validate_directory("dir1")


def test_validate_directory_exists_is_dir_returns_path():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'is_dir', lambda _: True)
        assert Path('dir1') == validate_directory("dir1")


def test_validate_directory_exists_not_dir_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'is_dir', lambda _: False)
        with pytest.raises(SystemExit):
            validate_directory("dir1")


def test_validate_directory_exists_returns_data_dir():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'is_dir', lambda _: True)
        assert Path('dir1') == validate_directory("dir1")
