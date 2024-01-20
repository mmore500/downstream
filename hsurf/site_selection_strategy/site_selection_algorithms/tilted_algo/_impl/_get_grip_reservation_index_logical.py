from .....pylib import longevity_ordering_naive as lon
from ._get_global_epoch import get_global_epoch
from ._get_global_num_reservations import get_global_num_reservations_at_epoch
from ._get_grip_reservation_index_physical import (
    get_grip_reservation_index_physical_at_epoch,
)


def get_grip_reservation_index_logical(
    grip: int,
    rank: int,
    surface_size: int,
) -> int:
    """Get the logical (persistence order) index of the grip's reservation at
    rank r.

    "grip" stands for genesis reservation index physical of a site.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    epoch = get_global_epoch(rank, surface_size)
    return get_grip_reservation_index_logical_at_epoch(
        grip, epoch, surface_size
    )


def get_grip_reservation_index_logical_at_epoch(
    grip: int,
    epoch: int,
    surface_size: int,
) -> int:
    """Get the logical (persistence order) index of the grip's reservation at
    epoch e.

    "grip" stands for genesis reservation index physical of a site.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    physical_idx = get_grip_reservation_index_physical_at_epoch(
        grip, epoch, surface_size
    )
    num_reservations = get_global_num_reservations_at_epoch(epoch, surface_size)
    res = lon.get_longevity_index_of_mapped_position(
        physical_idx, num_reservations
    )
    assert 0 <= res < num_reservations
    return res
