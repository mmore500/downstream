from .bit_invert import bit_invert


def bit_count_leading_ones(n: int) -> int:
    """Count the number of consecutive leading 1's in the binary representation
    of an integer.

    Examples
    --------
    >>> bit_count_leading_ones(0b11110000)
    4
    >>> bit_count_leading_ones(0b1111)
    4
    >>> bit_count_leading_ones(0b100000000)
    1
    """
    # see https://stackoverflow.com/a/77756334/17332200
    return n.bit_length() - bit_invert(n).bit_length()
