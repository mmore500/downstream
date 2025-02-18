import typing

from ..._auxlib._ctz import ctz
from ._compressing_has_ingest_capacity import compressing_has_ingest_capacity


def compressing_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for compressing curation.

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

        See `compressing_algo.has_ingest_capacity` for details.
    """
    if not compressing_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    if T == 0:
        return 0
    else:
        T -= 1

    si = (T // (S - 1)).bit_length()  # Current sampling interval
    h = ctz(T or 1)  # Current hanoi value

    if (h < si):
        return None

    return T % (S - 1) + 1


assign_storage_site = compressing_assign_storage_site  # lazy loader workaround
