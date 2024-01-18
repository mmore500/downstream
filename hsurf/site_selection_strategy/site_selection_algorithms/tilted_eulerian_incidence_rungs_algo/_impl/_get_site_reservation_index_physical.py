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

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    epoch = get_global_epoch(rank, surface_size)
    return get_site_reservation_index_physical_at_epoch(
        site, epoch, surface_size
    )


def get_site_reservation_index_physical_at_epoch(
    site: int,
    epoch: int,
    surface_size: int,
) -> int:
    """Get the physical index of the site's reservation at epoch e.

    Physical in the sense of as laid out on the surface from left to right.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= site < surface_size
    assert epoch >= 0

    ansatz = get_site_genesis_reservation_index_physical(site, surface_size)
    return fast_pow2_divide(ansatz, 1 << epoch)  # equiv 2 ** epoch
