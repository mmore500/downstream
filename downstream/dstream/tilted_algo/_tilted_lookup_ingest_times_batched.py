import numpy as np

from ..._auxlib._bit_floor_batched import bit_floor_batched
from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..._auxlib._bitlen32_scalar import bitlen32_scalar
from ..._auxlib._ctz_batched import ctz_batched

# from ..._auxlib._jit import jit
from ..._auxlib._modpow2 import modpow2


# @jit(nopython=True, parallel=True)
def tilted_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Ingest time lookup algorithm for tilted curation.

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
    assert (np.asarray(T) >= S).all()

    s = bitlen32_scalar(S) - 1
    t = bitlen32_batched(T).astype(T.dtype) - s  # Current epoch

    blt = bitlen32_batched(t).astype(T.dtype)  # Bit length of t
    # ^^^ why is this dtype cast necessary?
    epsilon_tau = bit_floor_batched(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch
    t0 = (1 << tau0) - tau0  # Opening epoch of current meta-epoch
    T0 = 1 << (t + s - 1)  # Opening time of current epoch

    M_ = np.maximum(S >> tau1, 1)
    # ^^^ Number of invading segments present at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = 0  # Assigned hanoi value of 0th site
    m_p = 0  # Left-to-right (physical) segment index
    res = np.zeros((T.size, S), dtype=np.uint64)
    for k in range(S):  # For each site in buffer...
        b_l = ctz_batched(M_ + m_p)  # Reverse fill order (logical) bunch index
        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment
        m_l_ = (M_ + m_p) >> (b_l + 1)  # Logical (fill order) segment index

        # Detect scenario...
        # Scenario A: site in invaded segment, h.v. ring buffer intact
        X_A = h_ - (t - t0) > w - w0  # To be invaded in future epoch t in tau?
        T_i = ((2 * m_l_ + 1) << h_) - 1  # When overwritten by invader?
        X_A_ = np.logical_and(h_ - (t - t0) == w - w0, T_i >= T)
        # ^^^ Invaded at this epoch?

        # Scenario B site in invading segment, h.v. ring buffer intact
        X_B = np.logical_and.reduce((t - t0 < h_, h_ < w0, t < S - s))
        # ^^^ At future epoch t in tau?
        T_r = T0 + T_i  # When is site refilled after ring buffer halves?
        X_B_ = np.logical_and.reduce(
            (h_ == t - t0, t < S - s, T_r >= T),
        )  # At this epoch?

        assert (np.asarray(X_A + X_A_ + X_B + X_B_) <= 1).all()
        # ^^^ scenarios are mutually exclusive

        # Calculate corrected values...
        epsilon_G = np.logical_or.reduce((X_A, X_A_, X_B, X_B_)) * M_
        epsilon_h = np.logical_or(X_A, X_A_) * (w - w0)
        epsilon_T = np.logical_or(X_A_, X_B_) * (T - T0)
        # ^^^ Snap back to start of epoch

        M = M_ + epsilon_G
        h = h_ - epsilon_h
        Tc = T - epsilon_T  # Corrected time
        m_l = np.where(
            np.logical_or(X_A, X_A_),
            (M_ + m_p),
            m_l_,
        )

        # Decode what h.v. instance fell on site k...
        j = ((Tc + (1 << h)) >> (h + 1)) - 1  # Num seen, less one
        i = j - modpow2(j - m_l + M, M)  # H.v. incidence resident at site k
        # ... then decode ingest time for that ith h.v. instance
        res[:, k] = ((2 * i + 1) << h) - 1  # True ingest time, Tbar_k

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        m_p += h_ == w  # Bump to next segment if current is filled
        h_ *= h_ != w  # Reset h.v. if segment is filled

    return res
