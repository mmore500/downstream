import numpy as np
import pytest

import pylib


def test_calc_dyadic_lcm_upper_bound():
    # Test with positive integers
    assert pylib.calc_dyadic_lcm_upper_bound(12, 18) == 108
    assert pylib.calc_dyadic_lcm_upper_bound(13, 17) == 221

    # Test with powers of 2
    assert pylib.calc_dyadic_lcm_upper_bound(16, 32) == 32

    # Test with one number being multiple of the other
    assert pylib.calc_dyadic_lcm_upper_bound(3, 9) == 27

    # Test with prime numbers
    assert pylib.calc_dyadic_lcm_upper_bound(5, 7) == 35

    # Test with one number being 1
    assert pylib.calc_dyadic_lcm_upper_bound(1, 20) == 20

    # Test with large numbers
    assert pylib.calc_dyadic_lcm_upper_bound(100, 500) == 25 * 125 * 4


def test_upper_bound_correctness():
    for a in range(1, 50):
        for b in range(1, 50):
            upper_bound = pylib.calc_dyadic_lcm_upper_bound(a, b)
            true_lcm = np.lcm(a, b)
            assert upper_bound >= true_lcm
            assert upper_bound % a == 0
            assert upper_bound % b == 0
