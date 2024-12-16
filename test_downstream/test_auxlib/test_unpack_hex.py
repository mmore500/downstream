import more_itertools
import numpy as np

from downstream._auxlib._unpack_hex import unpack_hex


def _big_to_little_endian(hex_str: str) -> str:
    return "".join(
        reversed(
            [
                "".join(chunk)
                for chunk in more_itertools.chunked(hex_str, 2, strict=True)
            ]
        )
    )


def _test_unpack_hex(hex_str: str, num_items: int, expected_output: list) -> None:
    np.testing.assert_array_equal(
        unpack_hex(hex_str, num_items),
        np.array(expected_output, dtype=np.uint64),
    )
    print(hex_str, _big_to_little_endian(hex_str))
    np.testing.assert_array_equal(
        unpack_hex(
            _big_to_little_endian(hex_str), num_items, byteorder="little"
        ),
        np.array(expected_output, dtype=np.uint64),
    )


def test_unpack_hex_valid_input():
    _test_unpack_hex("00FF00FABF00FF00", 2, [0x00FF00FA, 0xBF00FF00])


def test_unpack_hex_padded_result():
    _test_unpack_hex("AA55AA55AA", 1, [0xAA55AA55AA])


def test_unpack_hex_single_item():
    _test_unpack_hex("FFFFFFFFFFFFFFF0", 1, [0xFFFFFFFFFFFFFFF0])


def test_unpack_hex_multiple_items():
    _test_unpack_hex(
        "0123456789ABCDEF0123456789ABCDEF",
        2,
        [0x0123456789ABCDEF, 0x0123456789ABCDEF],
    )


def test_unpack_hex_short_hex_string():
    _test_unpack_hex("FF", 1, [0xFF])


def test_unpack_hex_4bit_items():
    _test_unpack_hex("A1B2C3D4", 8, [0xA, 0x1, 0xB, 0x2, 0xC, 0x3, 0xD, 0x4])


def test_unpack_hex_1bit_items():
    _test_unpack_hex("F8", 8, [1, 1, 1, 1, 1, 0, 0, 0])


def test_unpack_hex_2bit_items():
    _test_unpack_hex("F8", 4, [0x3, 3, 2, 0])
