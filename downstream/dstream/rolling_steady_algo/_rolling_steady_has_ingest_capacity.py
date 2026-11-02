from ._rolling_steady_get_ingest_capacity import (
    rolling_steady_get_ingest_capacity,
)


def rolling_steady_has_ingest_capacity(S: int, T: int) -> bool:
    """Does this algorithm have capacity to ingest at logical time T?

    Parameters
    ----------
    S : int
        Number of buffer sites available.
    T : int
        Queried nonnegative logical time.

    Returns
    -------
    bool
        True if S is a power of two, at least 4.
    """
    assert T >= 0
    ingest_capacity = rolling_steady_get_ingest_capacity(S)
    return ingest_capacity is None or T < ingest_capacity


# lazy loader workaround
has_ingest_capacity = rolling_steady_has_ingest_capacity
