import pytest

import pylib


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 3),
        (4, 1),
        (5, 5),
        (6, 3),
        (7, 7),
        (8, 1),
        (9, 9),
        (10, 5),
        (255, 255),
        (256, 1),
        (257, 257),
        (1234567890, 631256265),
    ],
)
def test_bit_reverse(input, expected_output):
    assert pylib.bit_reverse(input) == expected_output
