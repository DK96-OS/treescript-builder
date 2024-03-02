"""Testing String Validation Methods"""
import pytest
from input.string_validation import is_nonempty_str


@pytest.mark.parametrize(
    "test_input,expect", 
    [(None, False),
        (4, False),
        ({}, False),
        ([], False),
        ("", False),
        (" ", False),
        ("\n", False),
    ]
)
def test_is_nonempty_str_returns_false(test_input, expect):
    assert is_nonempty_str(test_input) == expect


@pytest.mark.parametrize(
    "test_input,expect", 
    [("1", True),
        ("a", True),
        ("test", True),
    ]
)
def test_is_nonempty_str_returns_true(test_input, expect):
    assert is_nonempty_str(test_input) == expect
