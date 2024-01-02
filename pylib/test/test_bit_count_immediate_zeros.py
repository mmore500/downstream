import itertools as it

import numpy as np
import pylib


# fmt: off
# https://oeis.org/A290255
A290255 = [
    0,1,0,2,1,0,0,3,2,1,1,0,0,0,0,4,3,2,2,1,1,1,1,0,0,0,0,0,0,0,0,5,4,3,3,2,2,2,
    2,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,5,4,4,3,3,3,3,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0
]
# fmt: on


# comparison implementation
def bit_count_immediate_zeros_reference(n: int) -> int:
    """Count the number of zeros immediately following the first binary digit
    of x."""
    return f"{n:b}1"[1:].index("1")  # fstring "1" ensures a trailing 1


def test_bit_count_immediate_zeros_reference_sequence():
    juxtaposed = zip(
        map(pylib.bit_count_immediate_zeros, it.count(1)),
        map(bit_count_immediate_zeros_reference, it.count(1)),
        A290255,
    )
    assert not any(map(np.ptp, juxtaposed))


def test_bit_count_immediate_zeros_reference_implementation():
    np.random.seed(0)
    test_indices = [
        0,
        1,
        2,
        *map(int, np.linspace(0, 2**32, 10**5, dtype=int)),
        *map(int, np.geomspace(1, 2**32, 10**5, dtype=int)),
        *map(int, np.random.randint(0, 2**32, 10**5)),
    ]
    juxtaposed = zip(
        map(pylib.bit_count_immediate_zeros, test_indices),
        map(bit_count_immediate_zeros_reference, test_indices),
    )
    all(it.starmap(int.__eq__, juxtaposed))
