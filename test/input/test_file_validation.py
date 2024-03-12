"""Testing File Validation Methods.
"""
import pytest
from pathlib import Path

from input.data_directory import DataDirectory
from input.file_validation import validate_input_file, validate_directory, get_file_extension


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ("file_name", "file_data"),
        ("file_name12", "file_data"),
    ]
)
def test_validate_input_file_returns_data(test_input, expect):
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: True)
        m.setattr(Path, 'read_text', lambda c: "file_data")
        assert validate_input_file(test_input) == expect


def test_validate_input_file_does_not_exist_raises_exit():
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: False)
        m.setattr(Path, 'read_text', lambda c: "")
        try:
            validate_input_file("file_name")
            assert False
        except SystemExit as e:
            assert True


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ("file_name", "file_data"),
        ("file_name12", "file_data"),
    ]
)
def test_validate_input_file_is_empty_returns_none(test_input, expect):
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: True)
        m.setattr(Path, 'read_text', lambda c: expect)
        assert validate_input_file(test_input) == expect


def test_validate_directory_does_not_exist_raises_exit():
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: False)
        try:
            validate_directory("dir1") == False
            assert False
        except SystemExit as e:
            assert True
    

def test_validate_directory_exists_returns_true():
    with pytest.MonkeyPatch().context() as m:
        m.setattr(Path, 'exists', lambda c: True)
        assert validate_directory("dir1") == DataDirectory(Path('dir1'))


@pytest.mark.parametrize(
    "test_input",
    [
        (''),
        (' '),
        ('file'),
        ('incorrect.'),
    ]
)
def test_get_file_extension_returns_none(test_input):
    assert get_file_extension(test_input) == None


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ('requirements.txt', 'txt'),
        ('__init__.py', 'py'),
        ('data_files.py', 'py'),
        ('ClassName.java', 'java'),
        ('archive.tar.gz', 'gz'),
    ]
)
def test_get_file_extension_returns_str(test_input, expect):
    assert get_file_extension(test_input) == expect
