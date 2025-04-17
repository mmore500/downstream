import typing

from ..._auxlib._ctz import ctz
from ..._auxlib._indexable_range import indexable_range
from ..compressing_algo._compressing_assign_storage_site import (
    compressing_assign_storage_site,
)
from ._xtctail_has_ingest_capacity import xtctail_has_ingest_capacity


def xtctail_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for xtctail curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.

    Raises
    ------
    ValueError
        If insufficient ingest capacity is available.

        See `xtctail_algo.has_ingest_capacity` for details.

    References
    ----------
    John C. Gunther. 2014. Algorithm 938: Compressing circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    if not xtctail_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    S, T = int(S), int(T)
    h = ctz(T + 1)  # Current hanoi value

    if T < S:  # handle initial fill
        hv_offset = (1 << h) - 1
        hv_cadence = 2 << h
        hvTs = indexable_range(hv_offset, S, hv_cadence)
        T_ = reversed(hvTs)[hvTs.index(T)]
        if (T_ + 1).bit_count() <= 1:
            return h
        else:
            # see https://oeis.org/A057716
            return S.bit_length() + T_ - T_.bit_length()
    elif h <= 1:
        return h

    epoch = (T + 1).bit_length()  # Current epoch
    si = ((epoch - 2) // (S - 1)).bit_length()  # Current sampling interval
    si_ = 1 << si
    assert si_
    prev_si_ = si_ >> 1

    cur_si_values = range(1, epoch, si_)
    num_cur_si = len(cur_si_values)

    if h % max(prev_si_, 1):
        return None
    elif h in cur_si_values or h == 0:
        return compressing_assign_storage_site(S, h)

    prev_si_values = reversed(
        indexable_range(1 + prev_si_, (S - 1) * prev_si_, si_),
    )
    try:
        min_prev_si = prev_si_values[S - 1 - num_cur_si - 1]
    except IndexError:
        min_prev_si = 0

    if min_prev_si <= h < (S - 1) * prev_si_:
        return compressing_assign_storage_site(S, h)
    else:
        return None


assign_storage_site = xtctail_assign_storage_site  # lazy loader workaround
