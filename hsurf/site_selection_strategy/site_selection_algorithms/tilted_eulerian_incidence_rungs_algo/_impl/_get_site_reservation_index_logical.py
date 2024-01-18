from .....pylib import longevity_ordering_naive as lon
from ._get_global_epoch import get_global_epoch
from ._get_global_num_reservations import get_global_num_reservations_at_epoch
from ._get_site_reservation_index_physical import (
    get_site_reservation_index_physical_at_epoch,
)


def get_site_reservation_index_logical(
    site: int,
    rank: int,
    surface_size: int,
) -> int:
    """Get the logical (persistence order) index of the site's reservation at
    rank r.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    epoch = get_global_epoch(rank, surface_size)
    return get_site_reservation_index_logical_at_epoch(
        site, epoch, surface_size
    )


def get_site_reservation_index_logical_at_epoch(
    site: int,
    epoch: int,
    surface_size: int,
) -> int:
    """Get the logical (persistence order) index of the site's reservation at
    epoch e.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    physical_idx = get_site_reservation_index_physical_at_epoch(
        site, epoch, surface_size
    )
    num_reservations = get_global_num_reservations_at_epoch(epoch, surface_size)
    res = lon.get_longevity_index_of_mapped_position(
        physical_idx, num_reservations
    )
    assert 0 <= res < num_reservations
    return res
