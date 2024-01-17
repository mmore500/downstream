from .....pylib import fast_pow2_divide

from ._get_global_epoch import get_global_epoch
from ._get_site_genesis_reservation_index_physical import (
    get_site_genesis_reservation_index_physical,
)


def get_site_reservation_index_physical(
    site: int,
    rank: int,
    surface_size: int,
) -> int:
    """Get the physical index of the site's reservation at rank r.

    Physical in the sense of as laid out on the surface from left to right.
    """
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= site < surface_size
    assert rank >= 0

    ansatz = get_site_genesis_reservation_index_physical(site, surface_size)
    epoch = get_global_epoch(rank, surface_size)
    return fast_pow2_divide(ansatz, epoch + 1)
