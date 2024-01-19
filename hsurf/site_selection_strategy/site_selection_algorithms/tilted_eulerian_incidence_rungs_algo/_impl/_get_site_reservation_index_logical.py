from ._get_grip_reservation_index_logical import (
    get_grip_reservation_index_logical,
    get_grip_reservation_index_logical_at_epoch,
)
from ._get_site_genesis_reservation_index_physical import (
    get_site_genesis_reservation_index_physical,
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
    grip = get_site_genesis_reservation_index_physical(site, surface_size)
    return get_grip_reservation_index_logical(grip, rank, surface_size)


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
    grip = get_site_genesis_reservation_index_physical(site, surface_size)
    return get_grip_reservation_index_logical_at_epoch(
        grip, epoch, surface_size
    )
