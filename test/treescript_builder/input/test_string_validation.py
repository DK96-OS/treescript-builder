""" Testing String Validation Methods
"""
import pytest

from test.treescript_builder.input.conftest import generate_filenames, generate_invalid_data_label_chars
from treescript_builder.input.string_validation import validate_name, validate_data_label, validate_dir_name


@pytest.mark.parametrize(
    "test_input,expect",
    [
        (None, False),
        (4, False),
        ({}, False),
        ([], False),
        ("", False),
        (" ", False),
        ("\n", False),
    ]
)
def test_validate_name_returns_false(test_input, expect):
    assert validate_name(test_input) == expect


@pytest.mark.parametrize(
    "test_input,expect",
    [
        ("1", True),
        ("a", True),
        ("test", True),
    ]
)
def test_validate_name_returns_true(test_input, expect):
    assert validate_name(test_input) == expect


def test_validate_name_filenames_returns_true():
    for filename in generate_filenames():
        assert validate_name(filename)


@pytest.mark.parametrize(
    "test_input",
    [
        '',
        ' ',
        ',',
        '-',
        '_',
        '.',
        '..',
        '*',
        '**',
        '=',
    ]
)
def test_validate_data_label_returns_false(test_input):
    assert not validate_data_label(test_input)


@pytest.mark.parametrize(
    "test_input", [
        '..\\',
        '../',
        r'.\.',
        'paths/are/invalid',
        'paths\\are\\invalid',
    ]
)
def test_validate_data_label_contains_slash_char_returns_false(test_input):
    assert not validate_data_label(test_input)


def test_validate_data_label_invalid_range_returns_false():
    for invalid_char in generate_invalid_data_label_chars():
        assert not validate_data_label(invalid_char)


@pytest.mark.parametrize(
    "test_input",
    [
        '1',
        'Name',
        'hello_file',
        'hello-file',
        'ClassName.java',
        'FileNumber23',
        'FileNumber23.txt',
    ]
)
def test_validate_data_label_returns_true(test_input):
    assert validate_data_label(test_input)


def test_validate_data_label_name_shortcut_returns_true():
    assert validate_data_label('!')


def test_validate_dir_name_returns_str():
    assert validate_dir_name('dir/') == 'dir'


def test_validate_dir_name_backslash_dir_returns_str():
    assert validate_dir_name('dir\\') == 'dir'


@pytest.mark.parametrize(
    "test_input",
    [
        '',
        ' ',
    ]
)
def test_validate_dir_name_special_inputs_returns_none(test_input):
    assert validate_dir_name(test_input) is None


def test_validate_dir_name_filenames_returns_none():
    for filename in generate_filenames():
        assert validate_dir_name(filename) is None # Filenames are not Dir Names.


def test_validate_dir_name_inconsistent_slash_chars_raises_error():
    with pytest.raises(ValueError):
        validate_dir_name('\\dir/')
