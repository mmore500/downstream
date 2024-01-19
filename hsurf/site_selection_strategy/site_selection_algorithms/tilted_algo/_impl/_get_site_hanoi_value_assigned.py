import typing

from ._get_grip_reservation_index_logical import (
    get_grip_reservation_index_logical,
)
from ._get_reservation_position_logical import get_reservation_position_logical
from ._get_site_genesis_reservation_index_physical import (
    get_site_genesis_reservation_index_physical,
)


def get_site_hanoi_value_assigned(
    site: int, rank: int, surface_size: int, grip: typing.Optional[int] = None
) -> int:
    """Get the Hanoi value assigned to a site at current epoch.

    "grip" stands for genesis reservation index physical of a site.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    if grip is None:
        grip = get_site_genesis_reservation_index_physical(site, surface_size)

    reservation_idx = get_grip_reservation_index_logical(
        grip, rank, surface_size
    )
    res = site - get_reservation_position_logical(reservation_idx, surface_size)
    assert 0 <= res
    return res
