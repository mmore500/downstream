from .....pylib import longevity_ordering_naive as lon
from ._get_reservation_position_physical import (
    get_reservation_position_physical,
)


def get_reservation_position_logical(
    reservation: int, surface_size: int
) -> int:
    """Return the zeroth site of the given reservation, indexed in logical
    order (persistence order)."""
    assert surface_size.bit_count() == 1  # power of 2
    num_reservations = surface_size >> 1
    physical_reservation = lon.get_longevity_mapped_position_of_index(
        reservation, num_reservations
    )
    return get_reservation_position_physical(
        physical_reservation, surface_size
    )
