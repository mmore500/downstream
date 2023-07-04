import math

from .sign import sign


def fast_pow2_divide(dividend: int, divisor: int) -> int:
    """Perform fast division using bitwise operations.

    Parameters
    ----------
    dividend : int
        The dividend of the division operation.
    divisor : int
        The divisor of the division operation. Must be a positive integer and a
        power of 2.

    Returns
    -------
    int
        The quotient of dividing the dividend by the divisor.

    Examples
    --------
    >>> fast_pow2_divide(16, 4)
    4

    >>> fast_pow2_divide(0, 4)
    0

    >>> fast_pow2_divide(15, 4)
    3
    """

    assert divisor >= 1, "Divisor must be greater than or equal to 1"
    assert divisor.bit_count() == 1, "Divisor must be a power of 2"

    # Count the number of trailing zeros, which is equivalent to log2(divisor)
    shift_amount = (divisor - 1).bit_count()

    # Perform fast division using right shift
    return sign(dividend) * (abs(dividend) >> shift_amount)
