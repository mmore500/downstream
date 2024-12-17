import sys
import typing

import numpy as np


def unpack_hex(
    hex_str: str,
    num_items: int,
    *,
    byteorder: typing.Literal["big", "little"] = "big",
) -> np.ndarray:
    """Unpacks a hexadecimal string into an array of 64-bit unsigned integers.

    This function interprets the input hexadecimal string as a sequence of bits,
    reshapes it to represent `num_items` items, and returns a NumPy array of
    64-bit unsigned integers.

    Parameters
    ----------
    hex_str : str
        Hexadecimal string to be unpacked.
    num_items : int
        Number of items to unpack from the hexadecimal data.
    byteorder : {"big", "little"}, default "big"
        The endianness of the hex string being passed in.

    Returns
    -------
    np.ndarray
        Array of unsigned integers representing the unpacked data.

    Notes
    -----
    - Hex data is assumed to be packed using big-endian byte order.
    - The function requires a runtime little-endian byte order.
    """

    if sys.byteorder != "little":
        raise NotImplementedError(
            "native big-endian byte order not yet supported",
        )

    if num_items == len(hex_str):
        # handle 4-bit values by processing ascii ordinals directly
        ascii_codes = np.fromstring(hex_str.lower(), dtype="S1", sep="").view(
            np.uint8,
        )

        digits = ascii_codes - ord("0")
        alphas = ascii_codes - (ord("a") - 10)
        result = np.where(digits < 10, digits, alphas)

        if byteorder == "little":
            result[::2] = result[-2::-2]
            result[1::2] = result[::-2]
        return result

    # unpack hex string into numpy bytes array
    bytes_array = np.frombuffer(
        bytes.fromhex(hex_str),
        count=len(hex_str) >> 1,
        dtype=np.uint8,
    )
    if byteorder == "little":
        bytes_array = bytes_array[::-1]

    if num_items == len(bytes_array):
        # for 1-byte values, we are done
        return bytes_array

    # unpack bits, creating array with one entry per bit value
    bits_array = np.unpackbits(bytes_array, bitorder="big")
    if num_items == len(bytes_array) * 8:
        # for 1-byte values, we are done
        return bits_array

    # for the general case,
    # reshape bits into subarrays `num_items` wide
    # then pack bits from each subarray into a single value
    item_bits_array = bits_array.reshape((num_items, -1))[:, ::-1]
    item_bytes_array = np.packbits(
        item_bits_array,
        axis=1,
        bitorder="little",
    )
    item_8bytes_array = np.pad(
        item_bytes_array,
        ((0, 0), (0, 8 - len(item_bytes_array[0]))),
        constant_values=0,
        mode="constant",
    )
    return np.frombuffer(item_8bytes_array.ravel(), dtype=np.uint64)
