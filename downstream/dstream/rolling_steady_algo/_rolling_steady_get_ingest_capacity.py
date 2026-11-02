import typing


def rolling_steady_get_ingest_capacity(S: int) -> typing.Optional[int]:
    """How many data item ingestions does this algorithm support?

    Returns None for unlimited ingestions if S is a power of two, at least 4.
    Otherwise, returns zero.

    See Also
    --------
    has_ingest_capacity : Capacity check for a particular logical time.
    """
    surface_size_ok = S.bit_count() == 1 and S >= 4
    return None if surface_size_ok else 0


# lazy loader workaround
get_ingest_capacity = rolling_steady_get_ingest_capacity
