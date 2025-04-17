import typing

from ..._auxlib._ctz import ctz
from ..compressing_algo._compressing_assign_storage_site import (
    compressing_assign_storage_site,
)
from ..compressing_algo._compressing_lookup_ingest_times import (
    compressing_lookup_ingest_times,
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
        hvTs = [*range(2**h - 1, S, 2 ** (h + 1))]  # TODO optimize
        assert T in hvTs
        T_ = hvTs[::-1][hvTs.index(T)]
        if (T_ + 1).bit_count() <= 1:
            return h
        else:
            # see https://oeis.org/A057716
            return S.bit_length() + T_ - T_.bit_length()
    else:
        epoch = (T + 1).bit_length()  # Current epoch

        retained_hvs = [*compressing_lookup_ingest_times(S, epoch)]
        if h in retained_hvs:  # TODO opt
            return compressing_assign_storage_site(S, h)
        else:
            return None


assign_storage_site = xtctail_assign_storage_site  # lazy loader workaround
