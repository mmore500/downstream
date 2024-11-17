import numpy as np

from ._jit import jit
from ._jit_nb_or_np import nb_or_np


@jit(nopython=True)
def bitlen32_batched(arr: np.ndarray) -> np.ndarray:
    """Calculate the bit length (number of bits) needed to represent each
    integer for 32-bit integer arrays.

    Parameters
    ----------
    arr : np.ndarray
        A NumPy array of unsigned integers. Maximum value should be less than
        2^53.

    Returns
    -------
    np.ndarray
        An array of the same shape as `arr` containing the bit lengths for each
        corresponding integer in `arr`.

    Notes
    -----
    Numba-compatible implementation.
    """
    assert np.asarray(np.asarray(arr) < (1 << 53)).all()
    assert np.asarray(np.asarray(arr) >= 0).all()
    return np.ceil(np.log2(arr + 1)).astype(nb_or_np.uint8)
