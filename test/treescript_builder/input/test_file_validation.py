""" Testing File Validation Methods.
"""
from pathlib import Path

import pytest

from test.treescript_builder.conftest import raise_exception
from treescript_builder.input import validate_input_file, validate_directory


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ("file_name", "file_data"),
        ("file_name12", "file_data"),
    ]
)
def test_validate_input_file_returns_data(test_input, expect):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: "file_data")
        assert validate_input_file(test_input) == expect


def test_validate_input_file_does_not_exist_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        with pytest.raises(SystemExit):
            validate_input_file("file_name")


def test_validate_input_file_oserror_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: raise_exception('oserror'))
        with pytest.raises(SystemExit):
            validate_input_file("file_name")


def test_validate_input_file_ioerror_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: raise_exception('ioerror'))
        with pytest.raises(SystemExit):
            validate_input_file("file_name")


def test_validate_input_file_typeerror_raises_typerror():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: raise_exception('typeerror'))
        with pytest.raises(TypeError):
            validate_input_file("file_name")


def test_validate_input_file_valueerror_raises_valueerror():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: raise_exception('valueerror'))
        with pytest.raises(ValueError):
            validate_input_file("file_name")


def test_validate_input_file_is_empty_returns_none():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: "")
        result = validate_input_file("file_name")
        assert result is None


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ("file_name", "file_data"),
        ("file_name12", "file_data"),
    ]
)
def test_validate_input_file_is_empty_returns_none(test_input, expect):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: expect)
        assert validate_input_file(test_input) == expect


def test_validate_directory_does_not_exist_raises_exit():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        try:
            validate_directory("dir1")
            assert False
        except SystemExit as e:
            assert True


def test_validate_directory_exists_returns_data_dir():
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        data_dir = validate_directory("dir1")
        assert data_dir is not None
        assert data_dir == Path('dir1')