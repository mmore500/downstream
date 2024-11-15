import sys

import numpy as np


def unpack_hex(hex_str: str, num_items: int) -> np.ndarray:
    """
    Unpacks a hexadecimal string into an array of 64-bit unsigned integers.

    This function interprets the input hexadecimal string as a sequence of bits,
    reshapes it to represent `num_items` items, and returns a NumPy array of
    64-bit unsigned integers.

    Parameters
    ----------
    hex_str : str
        Hexadecimal string to be unpacked.
    num_items : int
        Number of items to unpack from the hexadecimal data.

    Returns
    -------
    np.ndarray
        Array of 64-bit unsigned integers representing the unpacked data.

    Notes
    -----
    - The function assumes a little-endian byte order in the system.
    """
    if sys.byteorder != "little":
        raise NotImplementedError(
            "native big-endian byte order not yet supported",
        )

    bytes_array = np.frombuffer(
        bytes.fromhex(hex_str),
        count=len(hex_str) // 2,
        dtype=np.uint8,
    )
    bits_array = np.unpackbits(
        bytes_array,
        bitorder="big",
    )
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
    res = np.frombuffer(item_8bytes_array.ravel(), dtype=np.uint64)
    return res
