import typing

import numpy as np

from ..._auxlib._bit_floor32 import bit_floor32
from ..._auxlib._bitlen32 import bitlen32
from ..._auxlib._ctz32 import ctz32


def stretched_assign_storage_site_batched(
    S: typing.Union[int, np.ndarray], T: typing.Union[int, np.ndarray]
) -> np.ndarray:
    """Site selection algorithm for stretched curation.

    Parameters
    ----------
    S : int or np.ndarray
        Buffer size. Must be a power of two.
    T : int or np.ndarray
        Current logical time. Must be less than 2**S - 1.

    Returns
    -------
    np.ndarray
        Selected site, if any. Otherwise, S.
    """
    S, T = np.atleast_1d(S).astype(np.int64), np.atleast_1d(T).astype(np.int64)
    assert np.logical_and(S > 1, np.bitwise_count(S) == 1).all()
    # restriction <= 2 ** 52 might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    s = bitlen32(S) - 1
    blT = bitlen32(T)
    t = blT - np.minimum(blT, s)  # Current epoch
    assert (t >= 0).all()
    h = ctz32(T + 1)  # Current hanoi value
    i = T >> (h + 1)  # Hanoi value incidence (i.e., num seen)

    blt = bitlen32(t)  # Bit length of t
    epsilon_tau = bit_floor32(t << 1) > t + blt  # Correction factor
    tau = blt - epsilon_tau  # Current meta-epoch

    b_l = i  # Logical bunch index...
    # ... i.e., in order filled (increasing nestedness/decreasing init size r)

    # Need to calculate physical bunch index...
    # ... i.e., position among bunches left-to-right in buffer space
    v = bitlen32(b_l)  # Nestedness depth level of physical bunch
    w = (S >> v) * np.sign(v)
    # ^^^ Num bunches spaced between bunches in nest level
    o = w >> 1  # Offset of nestedness level in physical bunch order
    p = b_l - bit_floor32(b_l)  # Bunch position within nestedness level
    b_p = o + w * p  # Physical bunch index...
    # ... i.e., in left-to-right sequential bunch order

    # Need to calculate buffer position of b_p'th bunch
    epsilon_k_b = np.sign(b_l)  # Correction factor for zeroth bunch...
    # ... i.e., bunch r=s at site k=0
    k_b = (  # Site index of bunch
        (b_p << 1) + np.bitwise_count((S << 1) - b_p) - 1 - epsilon_k_b
    )

    b = np.maximum(S >> (tau + 1), 1)  # Num bunches available to h.v.
    return np.where(
        i >= b,  # If seen more than sites reserved to hanoi value...
        S,  # ... discard without storing
        k_b + h,  # Calculate placement site, h.v. h is offset within bunch
    )


# lazy loader workaround
assign_storage_site_batched = stretched_assign_storage_site_batched