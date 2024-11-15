import numpy as np

from ._bitlen32 import bitlen32


def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert (np.asarray(x) > 0).all()
    return bitlen32(x & -x) - 1
