from ._get_reservation_position_logical import get_reservation_position_logical
from ._get_site_reservation_index_logical import (
    get_site_reservation_index_logical,
)


def get_site_hanoi_value_assigned(
    site: int,
    rank: int,
    surface_size: int,
) -> int:
    """Get the Hanoi value assigned to a site at current epoch.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    reservation_idx = get_site_reservation_index_logical(
        site, rank, surface_size
    )
    res = site - get_reservation_position_logical(reservation_idx, surface_size)
    assert 0 <= res
    return res
