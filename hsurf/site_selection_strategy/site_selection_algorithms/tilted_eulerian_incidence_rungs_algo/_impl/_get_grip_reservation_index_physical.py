from .....pylib import fast_pow2_divide
from ._get_global_epoch import get_global_epoch


def get_grip_reservation_index_physical(
    grip: int,
    rank: int,
    surface_size: int,
) -> int:
    """Get the physical index of the grip's reservation at rank r.

    "grip" stands for genesis reservation index physical of a site.

    Physical in the sense of as laid out on the surface from left to right.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    epoch = get_global_epoch(rank, surface_size)
    return get_grip_reservation_index_physical_at_epoch(
        grip, epoch, surface_size
    )


def get_grip_reservation_index_physical_at_epoch(
    grip: int,
    epoch: int,
    surface_size: int,
) -> int:
    """Get the physical index of the grip's reservation at epoch e.

    "grip" stands for genesis reservation index physical.

    Physical in the sense of as laid out on the surface from left to right.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= grip < surface_size // 2
    assert epoch >= 0

    ansatz = grip
    return fast_pow2_divide(ansatz, 1 << epoch)  # equiv 2 ** epoch
