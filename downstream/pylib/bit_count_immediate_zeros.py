from .bit_drop_msb import bit_drop_msb


def bit_count_immediate_zeros(x: int) -> int:
    """Count the number of zeros immediately following the first binary digit
    of x.

    Equivalent to [OEIS:A290255](https://oeis.org/A290255).
    """
    return x.bit_length() - bit_drop_msb(x).bit_length() - bool(x)
