import pytest

from pylib import bit_invert


@pytest.mark.parametrize(
    "n, expected",
    [
        (0b0, 0b0),  # 0 becomes 0
        (0b1, 0b0),  # 1 becomes 0
        (0b10, 0b1),  # 2 becomes 1
        (0b11, 0b0),  # 3 becomes 0
        (0b100, 0b11),  # 4 becomes 3
        (0b101, 0b10),  # 5 becomes 2
        (0b110, 0b1),  # 6 becomes 1
        (0b111, 0b0),  # 7 becomes 0
        (0b1000, 0b111),  # 8 becomes 7
        (0b1001, 0b110),  # 9 becomes 6
        (0b1010, 0b101),  # 10 becomes 5
        (0b1011, 0b100),  # 11 becomes 4
        (0b1100, 0b11),  # 12 becomes 3
        (0b1101, 0b10),  # 13 becomes 2
        (0b1110, 0b1),  # 14 becomes 1
        (0b1111, 0b0),  # 15 becomes 0
        (0b10000, 0b1111),  # 16 becomes 15
        (0b100000, 0b11111),  # 32 becomes 31
        (0b1000000, 0b111111),  # 64 becomes 63
        (0b10000000, 0b1111111),  # 128 becomes 127
        (0b100000000, 0b11111111),  # 256 becomes 255
    ],
)
def test_bit_invert_known_values(n, expected):
    assert bit_invert(n) == expected
