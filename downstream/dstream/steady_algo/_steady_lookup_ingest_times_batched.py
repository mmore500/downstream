import warnings

import numpy as np
import polars as pl

from ..._auxlib._bitlen32 import bitlen32
from ..._auxlib._bitlen_pl import bitlen_pl
from ..._auxlib._collect_chunked import collect_chunked


def steady_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = True,
) -> np.ndarray:
    """Ingest time lookup algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : np.ndarray
        One-dimensional array of current logical times.
    parallel : bool, default True
        Should polars be applied to parallelize operations?

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

    if parallel and S > 128:
        warnings.warn(
            "Reverting to serial implementation for S > 128 "
            "due to segfault bug as of polars v1.16.0. "
            "See <https://github.com/pola-rs/polars/issues/14079>.",
        )
        parallel = False

    return [
        _steady_lookup_ingest_times_batched_numpy,
        _steady_lookup_ingest_times_batched_polars,
    ][bool(parallel)](S, T)


def _steady_lookup_ingest_times_batched_numpy(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for steady_lookup_ingest_times_batched."""
    assert S > 1 and int(S).bit_count() == 1
    # restriction <= 2 ** 52 (bitlen32 precision) might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    s = bitlen32(S).astype(np.int64) - 1
    t = bitlen32(T).astype(np.int64) - s  # Current epoch

    b = 0  # Bunch physical index (left-to right)
    m_b__ = 1  # Countdown on segments traversed within bunch
    b_star = True  # Have traversed all segments in bunch?
    k_m__ = s + 1  # Countdown on sites traversed within segment

    res = np.empty((T.size, S), dtype=T.dtype)
    for k in range(S):  # Iterate over buffer sites, except unused last one
        # Calculate info about current segment...
        epsilon_w = b == 0  # Correction on segment width if first segment
        # Number of sites in current segment (i.e., segment size)
        w = s - b + epsilon_w
        m = (1 << b) - m_b__  # Calc left-to-right index of current segment
        h_max = t + w - 1  # Max possible hanoi value in segment during epoch

        # Calculate candidate hanoi value...
        h_ = h_max - (h_max + k_m__) % w

        # Decode ingest time of assigned h.v. from segment index g, ...
        # ... i.e., how many instances of that h.v. seen before
        T_bar_k_ = ((2 * m + 1) << h_) - 1  # Guess ingest time
        epsilon_h = (T_bar_k_ >= T) * w  # Correction on h.v. if not yet seen
        h = h_ - epsilon_h  # Corrected true resident h.v.
        T_bar_k = ((2 * m + 1) << h) - 1  # True ingest time
        res[:, k] = T_bar_k

        # Update within-segment state for next site...
        k_m__ = (k_m__ or w) - 1  # Bump to next site within segment

        # Update h for next site...
        # ... only needed if not calculating h fresh every iter [[see above]]
        h_ += 1 - (h_ >= h_max) * w

        # Update within-bunch state for next site...
        m_b__ -= not k_m__  # Bump to next segment within bunch
        b_star = not (m_b__ or k_m__)  # Should bump to next bunch?
        b += b_star  # Do bump to next bunch, if any
        # Set within-bunch segment countdown, if bumping to next bunch
        m_b__ = m_b__ or (1 << (b - 1))

    return res


def _steady_lookup_ingest_times_batched_polars(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for steady_lookup_ingest_times_batched."""
    assert S > 1 and int(S).bit_count() == 1

    c_, l_ = pl.col, pl.lit

    df = pl.LazyFrame({"T": T})

    s = int(S).bit_length() - 1
    t = bitlen_pl(c_("T")) - l_(s)
    df = df.with_columns(t=t)

    b = 0  # Bunch physical index (left-to right)
    m_b__ = 1  # Countdown on segments traversed within bunch
    b_star = True  # Have traversed all segments in bunch?
    k_m__ = s + 1  # Countdown on sites traversed within segment

    for k in range(S):  # Iterate over buffer sites, except unused last one
        # Calculate info about current segment...
        epsilon_w = b == 0  # Correction on segment width if first segment
        # Number of sites in current segment (i.e., segment size)
        w = s - b + epsilon_w
        m = (1 << b) - m_b__  # Calc left-to-right index of current segment

        # Max possible hanoi value in segment during epoch
        h_max = c_("t") + l_(w - 1)
        df = df.with_columns(h_max=h_max)

        # Calculate candidate hanoi value...
        h_ = c_("h_max") - (c_("h_max") + l_(k_m__)) % l_(w)
        df = df.with_columns(h_=h_)

        # Decode ingest time of assigned h.v. from segment index g, ...
        # ... i.e., how many instances of that h.v. seen before
        T_bar_k_ = np.left_shift(l_(2 * m + 1), c_("h_")) - l_(1)
        df = df.with_columns(T_bar_k_=T_bar_k_)
        # ^^^ Guess ingest time

        epsilon_h = (c_("T_bar_k_") >= c_("T")) * l_(w)
        df = df.with_columns(epsilon_h=epsilon_h)
        # ^^^ Correction on h.v. if not yet seen

        h = c_("h_") - c_("epsilon_h")  # Corrected true resident h.v.
        df = df.with_columns(h=h)

        T_bar_k = np.left_shift(l_(2 * m + 1), c_("h")) - l_(1)
        # ^^^ True ingest time
        df = df.with_columns(T_bar_k.alias(f"{k}"))

        # Update within-segment state for next site...
        k_m__ = (k_m__ or w) - 1  # Bump to next site within segment

        # Update h for next site...
        # ... only needed if not calculating h fresh every iter [[see above]]
        h_ = c_("h_") + l_(1) - (c_("h_") >= c_("h_max")) * l_(w)
        df = df.with_columns(h_=h_)

        # Update within-bunch state for next site...
        m_b__ -= not k_m__  # Bump to next segment within bunch
        b_star = not (m_b__ or k_m__)  # Should bump to next bunch?
        b += b_star  # Do bump to next bunch, if any
        # Set within-bunch segment countdown, if bumping to next bunch
        m_b__ = m_b__ or (1 << (b - 1))

    df = df.select("^[0-9]+$")  # select only numbered Tbar_k "result" columns
    df = collect_chunked(df, len(T))  # uses polars threadpool
    return df.collect().to_numpy()


# lazy loader workaround
lookup_ingest_times_batched = steady_lookup_ingest_times_batched
