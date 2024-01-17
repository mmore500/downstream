from .....pylib import longevity_ordering_naive as lon

from ._get_global_num_reservations import get_global_num_reservations
from ._get_site_reservation_index_physical import (
    get_site_reservation_index_physical,
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
    physical_idx = get_site_reservation_index_physical(site, rank, surface_size)
    num_reservations = get_global_num_reservations(rank, surface_size)
    res = lon.get_longevity_index_of_mapped_position(
        physical_idx, num_reservations
    )
    assert 0 <= res < num_reservations
    return res
