import warnings

import numpy as np
import polars as pl

from ..._auxlib._bit_floor32 import bit_floor32
from ..._auxlib._bit_floor_pl import bit_floor_pl
from ..._auxlib._bitlen32 import bitlen32
from ..._auxlib._bitlen_pl import bitlen_pl
from ..._auxlib._bitwise_count64_batched import bitwise_count64_batched
from ..._auxlib._collect_chunked import collect_chunked
from ..._auxlib._ctz32 import ctz32


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
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    if parallel and S > 64:
        warnings.warn(
            "Reverting to serial implementation for S > 64 "
            "due to segfault bug as of polars v1.16.0. "
            "See <https://github.com/pola-rs/polars/issues/14079>.",
        )
        parallel = False

    return [
        _stretched_lookup_ingest_times_batched_numpy,
        _stretched_lookup_ingest_times_batched_polars,
    ][bool(parallel)](S, T)


def _stretched_lookup_ingest_times_batched_numpy(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for stretched_lookup_ingest_times_batched."""
    assert np.logical_and(
        np.asarray(S) > 1,
        bitwise_count64_batched(np.atleast_1d(np.asarray(S)).astype(np.uint64))
        == 1,
    ).all(), S
    # restriction <= 2 ** 52 (bitlen32 precision) might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    S = T.dtype.type(S)
    s = bitlen32(S) - 1
    t = bitlen32(T) - s  # Current epoch

    blt = bitlen32(t)  # Bit length of t
    epsilon_tau = bit_floor32(t.astype(np.uint64) << 1) > t + blt
    # ^^^ Correction factor
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
        b_l = ctz32(M + m_p)  # Logical bunch index...
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


def _lshift64(x: pl.Expr, y: pl.Expr) -> pl.Expr:
    return np.left_shift(
        x.cast(pl.UInt64),
        y.cast(pl.UInt64),
    )


def _rshift64(x: pl.Expr, y: pl.Expr) -> pl.Expr:
    return np.right_shift(
        x.cast(pl.UInt64),
        y.cast(pl.UInt64),
    )


def _stretched_lookup_ingest_times_batched_polars(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for stretched_lookup_ingest_times_batched."""
    assert S > 1 and int(S).bit_count() == 1

    c_, l_ = pl.col, pl.lit

    df = pl.LazyFrame({"T": T.astype(np.uint64)})

    s = bitlen32(S) - 1
    t = bitlen_pl(c_("T")) - l_(s)
    df = df.with_columns(t=t)

    blt = bitlen_pl(c_("t"))  # Bit length of t
    df = df.with_columns(blt=blt)
    epsilon_tau = (  # Correction factor
        bit_floor_pl(_lshift64(c_("t").cast(pl.UInt64), l_(1)))
        > c_("t") + c_("blt")
    ).cast(pl.UInt64)
    tau0 = blt - epsilon_tau  # Current meta-epoch
    df = df.with_columns(tau0=tau0)
    tau1 = tau0 + l_(1)  # Next meta-epoch
    df = df.with_columns(tau1=tau1)

    M = pl.max_horizontal(_rshift64(l_(S), c_("tau1")), l_(1).cast(pl.UInt64))
    # ^^^ Num invading segments at current epoch
    w0 = _lshift64(l_(1), c_("tau0")) - l_(1)
    # ^^^ Smallest segment size at current epoch start
    w1 = _lshift64(l_(1), c_("tau1")) - l_(1)
    # ^^^ Smallest segment size at next epoch start
    df = df.with_columns(M=M, w0=w0, w1=w1)

    h_ = l_(0).cast(pl.UInt64)  # Assigned hanoi value of 0th site
    m_p = l_(0).cast(pl.UInt64)
    # ^^^ Calc left-to-right index of 0th segment (physical segment idx)
    df = df.with_columns(h_=h_, m_p=m_p)

    for k in range(S):  # For each site in buffer...
        b_l = (c_("M") + c_("m_p")).cast(pl.UInt64).bitwise_trailing_zeros()
        # ^^^ Logical bunch index...
        # ... REVERSE fill order (decreasing nestedness/increasing init size r)

        epsilon_w = (  # Correction factor for segment size
            c_("m_p") == pl.lit(0)
        ).cast(pl.UInt64)
        df = df.with_columns(b_l=b_l, epsilon_w=epsilon_w)

        w = c_("w1") + c_("b_l") + c_("epsilon_w")
        # ^^^ Number of sites in current segment
        df = df.with_columns(w=w)

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = _rshift64(c_("M") + c_("m_p"), c_("b_l") + l_(1))
        df = df.with_columns(i_=i_)
        # ^^^ Guess h.v. incidence (i.e., num seen)
        Tbar_k_ = pl.max_horizontal(  # Guess ingest time
            _lshift64(l_(2) * c_("i_") + l_(1), c_("h_")) - l_(1),
            _lshift64(l_(1), c_("h_")) - l_(1),
            # ^^^ catch overflow
        )
        df = df.with_columns(Tbar_k_=Tbar_k_)

        epsilon_h = (  # Correction factor, h
            (c_("Tbar_k_") >= c_("T")).cast(pl.UInt64) * (c_("w") - c_("w0"))
        ).cast(pl.UInt64)

        epsilon_i = (  # Correction factor, i
            (c_("Tbar_k_") >= c_("T")).cast(pl.UInt64)
            * (c_("m_p") + c_("M") - c_("i_"))
        ).cast(pl.UInt64)
        df = df.with_columns(epsilon_h=epsilon_h, epsilon_i=epsilon_i)

        # Decode ingest time for ith instance of assigned h.v.
        h = c_("h_") - c_("epsilon_h")  # True hanoi value
        i = c_("i_") + c_("epsilon_i")  # True h.v. incidence
        df = df.with_columns(h=h, i=i)
        Tbar_k = (  # True ingest time, Tbar_k
            _lshift64(l_(2) * c_("i") + l_(1), c_("h")) - l_(1)
        ).cast(pl.UInt64)
        df = df.with_columns(Tbar_k.alias(f"{k}"))

        # Update state for next site...
        h_ = c_("h_") + l_(1)  # Assigned h.v. increases within each segment
        df = df.with_columns(h_=h_)
        # Bump to next segment if current is filled
        m_p = c_("m_p") + (c_("h_") == c_("w")).cast(pl.UInt64)
        h_ = c_("h_") * (c_("h_") != c_("w")).cast(pl.UInt64)
        # ^^^ Reset h.v. if segment is filled
        df = df.with_columns(m_p=m_p, h_=h_)

    df = df.select("^[0-9]+$")  # select only numbered Tbar_k "result" columns
    df = collect_chunked(df, len(T))  # uses polars threadpool
    return df.collect().to_numpy()


# lazy loader workaround
lookup_ingest_times_batched = stretched_lookup_ingest_times_batched
