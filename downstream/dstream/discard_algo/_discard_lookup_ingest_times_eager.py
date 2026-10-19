import typing


def discard_lookup_ingest_times_eager(
    S: int, T: int
) -> typing.List[typing.Optional[int]]:
    """Ingest time lookup algorithm for discard curation.

    Eager implementation.

    Parameters
    ----------
    S : int
        Buffer size. Must be positive.
    T : int
        Current logical time.

    Returns
    -------
    typing.List[typing.Optional[int]]
        Ingest time of stored item at buffer sites in index order.
    """
    assert T >= 0
    return [None] * S


# lazy loader workaround
lookup_ingest_times_eager = discard_lookup_ingest_times_eager
