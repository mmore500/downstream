import itertools as it
import typing

from ..compressing_algo._compressing_lookup_ingest_times import (
    compressing_lookup_impl,
)


def xtc_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for xtc curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Yields
    ------
    typing.Optional[int]
        Ingest time of stored item at buffer sites in index order.
    """
    assert T >= 0
    if T < S:  # Patch for before buffer is filled...
        return (v if v < T else None for v in xtc_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        return xtc_lookup_impl(S, T)


def xtc_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `xtc_lookup_ingest_times`."""
    S, T = int(S), int(T)  # play nice with numpy types
    assert S > 1 and S.bit_count() == 1
    assert T >= S  # T < S handled by T = S via xtc_lookup_ingest_times

    epoch = (T - 1).bit_length() + 1
    for x in it.islice(
        compressing_lookup_impl(S, max(epoch, S)),
        epoch,
    ):
        yield (bool(x) << x) >> 1

    for k in range(epoch, S):
        # https://oeis.org/A057716
        x = k - S.bit_length() + 1
        yield x + (x + x.bit_length()).bit_length()


lookup_ingest_times = xtc_lookup_ingest_times  # lazy loader workaround
