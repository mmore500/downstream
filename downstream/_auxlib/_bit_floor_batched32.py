import numpy as np

from ._bitlen32_batched import bitlen32_batched
from ._jit import jit


@jit(nogil=True, nopython=True)
def bit_floor_batched32(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    mask = np.uint64(1) << bitlen32_batched(n >> 1)
    return n & mask
