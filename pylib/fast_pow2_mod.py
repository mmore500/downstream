def fast_pow2_mod(dividend: int, divisor: int) -> int:
    """Perform fast mod using bitwise operations.

    Parameters
    ----------
    dividend : int
        The dividend of the mod operation. Must be a non-negative integer.
    divisor : int
        The divisor of the mod operation. Must be a positive integer and a
        power of 2.

    Returns
    -------
    int
        The remainder of dividing the dividend by the divisor.

    Examples
    --------
    >>> fast_pow2_mod(16, 4)
    0

    >>> fast_pow2_mod(17, 4)
    1

    >>> fast_pow2_mod(0, 4)
    0

    >>> fast_pow2_mod(3, 4)
    3
    """
    assert dividend >= 0
    assert divisor >= 1
    assert divisor.bit_count() == 1
    return dividend & (divisor - 1)  # calculate remainder
