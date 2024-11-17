import numpy as np

from ..._auxlib._bit_floor_batched import bit_floor_batched
from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..._auxlib._bitlen32_scalar import bitlen32_scalar
from ..._auxlib._ctz_batched import ctz_batched
from ..._auxlib._jit import jit


@jit(nopython=True, parallel=True)
def stretched_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Ingest time lookup algorithm for stretched curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : np.ndarray
        One-dimensional array of current logical times.

    Returns
    -------
    np.ndarray
        Ingest time of stored items at buffer sites in index order.

        Two-dimensional array. Each row corresponds to an entry in T. Contains
        S columns, each corresponding to buffer sites.
    """
    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    s = bitlen32_scalar(S) - 1
    t = bitlen32_batched(T).astype(T.dtype) - s  # Current epoch

    blt = bitlen32_batched(t).astype(T.dtype)  # Bit length of t
    epsilon_tau = bit_floor_batched(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch

    M = np.maximum((S >> tau1), 1)  # Num invading segments at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Assigned hanoi value of 0th site
    m_p = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Calc left-to-right index of 0th segment (physical segment idx)

    res = np.zeros((T.size, S), dtype=np.uint64)
    for k in range(S):  # For each site in buffer...
        b_l = ctz_batched(M + m_p)  # Logical bunch index...
        # ... REVERSE fill order (decreasing nestedness/increasing init size r)

        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (M + m_p) >> (b_l + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_k_ = ((2 * i_ + 1) << h_) - 1  # Guess ingest time
        epsilon_h = (Tbar_k_ >= T) * (w - w0)  # Correction factor, h
        epsilon_i = (Tbar_k_ >= T) * (m_p + M - i_)  # Correction factor, i

        # Decode ingest time for ith instance of assigned h.v.
        h = h_ - epsilon_h  # True hanoi value
        i = i_ + epsilon_i  # True h.v. incidence
        res[:, k] = ((2 * i + 1) << h) - 1  # True ingest time, Tbar_k

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        # Bump to next segment if current is filled
        m_p += (h_ == w).astype(T.dtype)
        h_ *= (h_ != w).astype(T.dtype)  # Reset h.v. if segment is filled

    return res
