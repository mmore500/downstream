from ._get_grip_reservation_index_physical import (
    get_grip_reservation_index_physical,
    get_grip_reservation_index_physical_at_epoch,
)
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
    grip = get_site_genesis_reservation_index_physical(site, surface_size)
    return get_grip_reservation_index_physical(grip, rank, surface_size)


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
    grip = get_site_genesis_reservation_index_physical(site, surface_size)
    return get_grip_reservation_index_physical_at_epoch(
        grip, epoch, surface_size
    )
