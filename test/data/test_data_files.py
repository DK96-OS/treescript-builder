"""Testing Data File Methods.
"""
import pytest

from data.data_files import get_file_extension, is_valid_data_label


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


@pytest.mark.parametrize(
    "test_input",
    [
        (''),
        (' '),
        ('!'),
        (','),
        ('-'),
        ('_'),
        ('.'),
        ('..'),
        ('*'),
        ('paths/are/invalid'),
        ('paths\\are\\invalid'),
        ('='),
    ]
)
def test_is_valid_data_label_returns_false(test_input):
    assert is_valid_data_label(test_input) == False


@pytest.mark.parametrize(
    "test_input",
    [
        ('1'),
        ('Name'),
        ('hello_file'),
        ('hello-file'),
        ('ClassName.java'),
        ('FileNumber23'),
        ('FileNumber23.txt'),
    ]
)
def test_is_valid_data_label_returns_true(test_input):
    assert is_valid_data_label(test_input) == True
