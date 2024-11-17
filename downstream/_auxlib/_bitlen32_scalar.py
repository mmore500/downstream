import numpy as np

from ._jit import jit
from ._jit_nb_or_np import nb_or_np


@jit(nopython=True)
def bitlen32_scalar(val: int) -> np.uint8:
    """Calculate the bit length (number of bits) needed to represent a single
    integer of numpy type.

    Parameters
    ----------
    vaal : np.{int32, int64, uint32, etc.}
        A NumPy  integers. Maximum value should be less than 2^53.

    Returns
    -------
    np.ndarray
        An array of the same shape as `arr` containing the bit lengths for each
        corresponding integer in `arr`.

    Notes
    -----
    Numba-compatible implementation.
    """
    assert val < (1 << 53)
    return nb_or_np.uint8(np.ceil(np.log2(val + 1)))
