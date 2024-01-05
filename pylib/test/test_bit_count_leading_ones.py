import pytest

import pylib


@pytest.mark.parametrize(
    "n, expected",
    [
        (0b0, 0),  # No leading ones in 0
        (0b1, 1),  # Single leading one
        (0b11, 2),  # Two leading ones
        (0b111, 3),  # Three leading ones
        (0b101, 1),  # Leading one followed by zero
        (0b1001, 1),  # Leading one followed by zeros and then another one
        (0b1011, 1),  # Leading one followed by zeros and then two ones
        (0b1101, 2),  # Two leading ones followed by zeros
        (0b11110000, 4),  # Four leading ones followed by zeros
        (0b10000000, 1),  # One leading one followed by many zeros
    ],
)
def test_bit_count_leading_ones(n, expected):
    assert pylib.bit_count_leading_ones(n) == expected
