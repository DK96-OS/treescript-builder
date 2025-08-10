""" Testing String Validation Methods
"""
import pytest

from treescript_builder.input.string_validation import validate_name, validate_data_label, validate_dir_name


@pytest.mark.parametrize(
    "test_input",
    [
        None,
        4,
        {},
        [],
        "",
        " ",
        "\n",
    ]
)
def test_validate_name_returns_false(test_input):
    assert not validate_name(test_input)


@pytest.mark.parametrize(
    "test_input",
    [
        "1",
        "a",
        "test",
        "dir/file.txt",
        "dir/dir2/file",
    ]
)
def test_validate_name_returns_true(test_input):
    assert validate_name(test_input)


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
        'paths/are/invalid',
        'paths\\are\\invalid',
        '=',
    ]
)
def test_validate_data_label_returns_false(test_input):
    assert not validate_data_label(test_input)


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


def test_validate_dir_name_empty_str_returns_none():
    assert validate_dir_name('') is None


def test_validate_dir_name_space_char_returns_none():
    assert validate_dir_name(' ') is None


def test_validate_dir_name_is_file_returns_none():
    assert validate_dir_name('file') is None


def test_validate_dir_name_inconsistent_slash_chars_raises_error():
    with pytest.raises(ValueError):
        validate_dir_name('\\dir/')
