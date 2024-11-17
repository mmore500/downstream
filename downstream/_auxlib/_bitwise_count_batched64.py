import numpy as np

from ._bitwise_count_batched32 import bitwise_count_batched32
from ._jit import jit


@jit("uint8[:](uint64[:])", nopython=True)
def bitwise_count_batched64(v: np.ndarray) -> np.ndarray:
    """Numba-friendly population count function for 64-bit integers."""
    front = v.astype(np.uint32)
    back = (v >> np.uint64(32)).astype(np.uint32)
    return bitwise_count_batched32(front) + bitwise_count_batched32(back)
