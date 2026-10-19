import typing

from ._discard_has_ingest_capacity import discard_has_ingest_capacity


def discard_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for discard curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be positive.
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

        See `discard_algo.has_ingest_capacity` for details.
    """
    if not discard_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    return None


assign_storage_site = discard_assign_storage_site  # lazy loader workaround
