"""Testing String Validation Methods"""
import pytest
from input.string_validation import validate_name, validate_data_label


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
def test_validate_data_label_returns_false(test_input):
    assert validate_data_label(test_input) == False


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
def test_validate_data_label_returns_true(test_input):
    assert validate_data_label(test_input) == True
