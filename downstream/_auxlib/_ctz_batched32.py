import numpy as np

from ._bitlen32_batched import bitlen32_batched
from ._jit import jit


@jit(nogil=True, nopython=True)
def ctz_batched32(x: np.ndarray) -> np.ndarray:
    """Count trailing zeros."""
    return bitlen32_batched(x & -x) - 1
