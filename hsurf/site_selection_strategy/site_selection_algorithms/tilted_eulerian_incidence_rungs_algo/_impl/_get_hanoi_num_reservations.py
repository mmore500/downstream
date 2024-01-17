from .....pylib import hanoi
from ._get_global_epoch import get_global_epoch
from ._get_global_num_reservations import get_global_num_reservations
from ._get_reservation_position_physical import (
    get_reservation_position_physical,
)


def get_hanoi_num_reservations(rank: int, surface_size: int) -> int:
    """Return the number of reservations remaining at the given rank.

    Either the current global-level reservation count, or double it if the
    hanoi value is uninvaded."""
    epoch = get_global_epoch(rank, surface_size)
    grc = get_global_num_reservations(rank, surface_size)

    if epoch == 0:
        return grc

    hanoi_value = hanoi.get_hanoi_value_at_index(rank)
    max_uninvaded = (1 << epoch) - 2  # 0, 2, 6, 14, ...
    assert max_uninvaded >= 0
    if hanoi_value > max_uninvaded:
        return grc

    reservation0_at = hanoi.get_max_hanoi_value_through_index(rank)
    assert epoch > 0
    idx = 1 << (epoch - 1)  # 1, 2, 4, 8, ...
    assert idx > 0
    reservation0_begin = get_reservation_position_physical(idx, surface_size)
    reservation0_progress = reservation0_at - reservation0_begin
    if hanoi_value <= reservation0_progress:
        return grc

    return 2 * grc
