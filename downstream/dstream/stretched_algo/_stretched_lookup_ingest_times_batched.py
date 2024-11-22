import warnings

import numpy as np

from ..._auxlib._bit_floor_batched32 import bit_floor_batched32
from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..._auxlib._bitlen32_scalar import bitlen32_scalar
from ..._auxlib._bitwise_count_batched64 import bitwise_count_batched64
from ..._auxlib._ctz_batched32 import ctz_batched32
from ..._auxlib._jit import jit


def stretched_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = True,
) -> np.ndarray:
    """Ingest time lookup algorithm for stretched curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : np.ndarray
        One-dimensional array of current logical times.
    parallel : bool, default True
        Should numba be applied to parallelize operations?

    Returns
    -------
    np.ndarray
        Ingest time of stored items at buffer sites in index order.

        Two-dimensional array. Each row corresponds to an entry in T. Contains
        S columns, each corresponding to buffer sites.
    """
    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    if parallel and T.size:
        if (
            int(T.max()) < 2**32 and int(S) <= 2**12
        ):  # 2**12 is max tested S
            return _stretched_lookup_ingest_times_batched_parallel(S, T)
        else:
            warnings.warn(
                "T too large; due to numba limitations in handling overflows, "
                "falling back to serial processing."
            )

    return _stretched_lookup_ingest_times_batched_serial(S, T)


def _stretched_lookup_ingest_times_batched_serial(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for stretched_lookup_ingest_times_batched."""
    assert np.logical_and(
        np.asarray(S) > 1,
        bitwise_count_batched64(np.atleast_1d(np.asarray(S)).astype(np.uint64))
        == 1,
    ).all(), S
    # restriction <= 2 ** 52 (bitlen32 precision) might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    s = T.dtype.type(bitlen32_scalar(S)) - 1
    t = bitlen32_batched(T).astype(T.dtype) - s  # Current epoch

    blt = bitlen32_batched(t).astype(T.dtype)  # Bit length of t
    epsilon_tau = bit_floor_batched32(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch

    M = np.maximum((S >> tau1), 1)  # Num invading segments at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Assigned hanoi value of 0th site
    m_p = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Calc left-to-right index of 0th segment (physical segment idx)

    res = np.empty((T.size, S), dtype=np.uint64)
    for k in range(S):  # For each site in buffer...
        b_l = ctz_batched32(M + m_p).astype(T.dtype)  # Logical bunch index...
        # ... REVERSE fill order (decreasing nestedness/increasing init size r)

        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (M + m_p) >> (b_l + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_k_ = np.maximum(  # Guess ingest time
            ((2 * i_ + 1).astype(np.uint64) << h_.astype(np.uint64)) - 1,
            (np.uint64(1) << h_.astype(np.uint64)) - 1,  # catch overflow
        )
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


@jit(nogil=True, nopython=True, parallel=True)
def _stretched_lookup_ingest_times_batched_parallel(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for stretched_lookup_ingest_times_batched."""
    assert np.logical_and(
        np.asarray(S) > 1,
        bitwise_count_batched64(np.atleast_1d(np.asarray(S)).astype(np.uint64))
        == 1,
    ).all(), S
    assert (np.maximum(S, T) <= 2**32).all()

    S, T = np.int64(S), T.astype(np.int64)  # patch for numba type limitations
    s = T.dtype.type(bitlen32_scalar(S)) - 1
    t = bitlen32_batched(T).astype(T.dtype) - s  # Current epoch

    blt = bitlen32_batched(t).astype(T.dtype)  # Bit length of t
    epsilon_tau = (
        bit_floor_batched32(t << 1).astype(T.dtype) > t + blt
    )  # Correction factor
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
        b_l = ctz_batched32(M + m_p).astype(T.dtype)  # Logical bunch index...
        # ... REVERSE fill order (decreasing nestedness/increasing init size r)

        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (M + m_p) >> (b_l + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_k_ = ((2 * i_ + 1) << h_) - 1  # Guess ingest time
        assert (Tbar_k_ >= (np.uint64(1) << h_.astype(np.uint64)) - 1).all()
        # ^^^ catch overflow
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


# lazy loader workaround
lookup_ingest_times_batched = stretched_lookup_ingest_times_batched
