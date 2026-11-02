import typing

from ..steady_algo._steady_lookup_ingest_times import (
    steady_lookup_ingest_times,
)
from ._rolling_steady_assign_storage_site import _select_sample
from ._rolling_steady_has_ingest_capacity import (
    rolling_steady_has_ingest_capacity,
)


def rolling_steady_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Reconstruct ingest times by physical site for rolling/steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two, at least 4.
    T : int
        Number of arrivals ingested so far.

    Returns
    -------
    typing.Iterable[typing.Optional[int]]
        Ingest times in buffer-site order; None marks an unwritten site.

    Notes
    -----
    Reconstruction uses O(S) word operations and temporary output storage.
    The timestamps are computed output, never persistent metadata. The
    iterable interface matches other algorithms, but computation is eager.
    """
    S, T = int(S), int(T)  # play nice with numpy types
    if not rolling_steady_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")
    m = S >> 1
    b = max(0, T - m)
    result = [None] * S
    for k in steady_lookup_ingest_times(m, b):
        if k is not None:
            result[_select_sample(m, k)] = k
    for k in range(b, T):
        result[_select_sample(m, k)] = k
    return iter(result)


# lazy loader workaround
lookup_ingest_times = rolling_steady_lookup_ingest_times
