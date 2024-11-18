import numpy as np

from ._bitwise_count_batched64 import bitwise_count_batched64
from ._jit import jit


@jit(nogil=True, nopython=True)
def modpow2_batched(dividend: np.ndarray, divisor: np.ndarray) -> np.ndarray:
    """Perform fast mod using bitwise operations.

    Parameters
    ----------
    dividend : np.ndarray
        The dividend of the mod operation. Must be positive integers.
    divisor : np.ndarray
        The divisor of the mod operation. Must be positive integers and an even
        power of 2.

    Returns
    -------
    np.ndarray
        The remainder of dividing the dividends by the divisors.

    Notes
    -----
    Numba-compatible implementation.
    """
    # Assert divisor is a power of two
    assert (bitwise_count_batched64(divisor.astype(np.uint64)) == 1).all()
    return dividend & (divisor - 1)
