import numpy as np

from .count_factors_of_2 import count_factors_of_2


def calc_dyadic_lcm_upper_bound(a: int, b: int) -> int:
    """Calculate an upper bound of the least common multiple (LCM) of two
    integers as their product less their common factors of 2.

    Returns
    -------
    int
        The upper bound of the LCM of `a` and `b` obtained by removing
        the common factors of 2.

    Examples
    --------
    >>> calc_dyadic_lcm_upper_bound(12, 18)
    108
    >>> calc_dyadic_lcm_upper_bound(13, 17)
    221
    """
    assert a
    assert b
    least_factors_of_2 = min(count_factors_of_2(a), count_factors_of_2(b))
    res = a * b >> least_factors_of_2
    return res
