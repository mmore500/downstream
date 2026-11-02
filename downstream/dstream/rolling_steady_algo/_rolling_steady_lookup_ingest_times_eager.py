import typing

from ._rolling_steady_lookup_ingest_times import (
    rolling_steady_lookup_ingest_times,
)


def rolling_steady_lookup_ingest_times_eager(
    S: int, T: int
) -> typing.List[int]:
    """Reconstruct ingest times for a filled rolling/steady buffer.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two, at least 4.
    T : int
        Number of arrivals ingested so far. Must be at least S.

    Returns
    -------
    typing.List[int]
        Ingest times in buffer-site order.
    """
    if T < S:
        raise ValueError("T < S not supported for eager lookup")
    return list(rolling_steady_lookup_ingest_times(S, T))


# lazy loader workaround
lookup_ingest_times_eager = rolling_steady_lookup_ingest_times_eager
