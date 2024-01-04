def bit_invert(n: int) -> int:
    """Calculate the bitwise inverse of n.

    Doesn't do funky stuff with sign bits, like Python's built-in bitwise not.
    """
    mask = (1 << n.bit_length()) - 1
    return n ^ mask
