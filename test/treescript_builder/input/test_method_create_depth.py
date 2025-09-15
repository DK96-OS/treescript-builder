""" Testing Conftest Data Provider Method: create_depth.
"""
import pytest

from test.treescript_builder.conftest import create_depth


@pytest.mark.parametrize(
    "test_input,expect",
    [
        (0, 0),
        (1, 2),
        (2, 4),
        (4, 8),
    ]
)
def test_create_depth_returns_expected(test_input, expect):
    assert len(create_depth(test_input)) == expect


def test_create_depth_negative_numbers_returns_empty():
    assert '' == create_depth(-1)
