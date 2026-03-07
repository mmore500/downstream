import numpy as np

from downstream._auxlib._unpack_hex_bits import unpack_hex_bits


def test_unpack_hex_bits_single_hex_char():
    result = unpack_hex_bits("f")
    np.testing.assert_array_equal(result, [1, 1, 1, 1])


def test_unpack_hex_bits_zero():
    result = unpack_hex_bits("0")
    np.testing.assert_array_equal(result, [0, 0, 0, 0])


def test_unpack_hex_bits_two_chars():
    result = unpack_hex_bits("0f")
    np.testing.assert_array_equal(
        result, [0, 0, 0, 0, 1, 1, 1, 1],
    )


def test_unpack_hex_bits_odd_length():
    # odd-length hex: "a" -> 1010
    result = unpack_hex_bits("a")
    np.testing.assert_array_equal(result, [1, 0, 1, 0])


def test_unpack_hex_bits_even_length():
    result = unpack_hex_bits("ff")
    np.testing.assert_array_equal(result, [1] * 8)


def test_unpack_hex_bits_longer():
    result = unpack_hex_bits("00ff")
    assert len(result) == 16
    np.testing.assert_array_equal(result[:8], [0] * 8)
    np.testing.assert_array_equal(result[8:], [1] * 8)
