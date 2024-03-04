"""Testing Input Module
"""
import pytest


SPACE_CHARS = (' ', ' ', ' ', ' ')


def create_depth(depth: int) -> str:
    """Creates a string of space chars equivalent to the given depth.

	Parameters:
	- depth (int): The amount of depth in the Tree Node Structure.

	Returns:
	str: The String of a Space Char, of the required length.
	"""
    return SPACE_CHARS[0] * depth * 2


@pytest.mark.parametrize(
    "test_input,expect", 
    [
        (0, 0),
        (1, 2),
        (2, 4),
        (4, 8),
    ]
)
def test_validate_name_returns_true(test_input, expect):
    assert len(create_depth(test_input)) == expect
