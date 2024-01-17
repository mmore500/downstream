from .....pylib import hanoi, oeis

from ._get_global_num_reservations import get_global_num_reservations
from ._get_reservation_position_physical import (
    get_reservation_position_physical,
)


def get_site_genesis_reservation_index_physical(
    site: int,
    surface_size: int,
) -> int:
    """Get the physical index of the site's reservation at rank 0.

    Physical in the sense of as laid out on the surface from left to right.

    Does not take into account incidence-level runging (i.e., sweep over time
    as new reservation grows).
    """
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= site < surface_size

    r0_size = get_reservation_position_physical(1, surface_size)  # excl extra
    base_index = hanoi.get_hanoi_value_index_offset(r0_size)
    base_value = oeis.get_a005187_value_at_index(base_index)

    lookup_value = site + base_value
    res = oeis.get_a005187_index_of_value(lookup_value) - base_index
    assert 0 <= res < get_global_num_reservations(0, surface_size)
    return res
