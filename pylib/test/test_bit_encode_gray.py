import pytest

import pylib


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (0, 0),
        (1, 1),
        (2, 3),
        (3, 2),
        (4, 6),
        (5, 7),
        (6, 5),
        (7, 4),
        (8, 12),
        (9, 13),
        (10, 15),
        (255, 128),
        (256, 384),
        (257, 385),
        (1234567890, 1834812347),
    ],
)
def test_bit_encode_gray(input, expected_output):
    assert pylib.bit_encode_gray(input) == expected_output
