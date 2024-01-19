from .....pylib import hanoi


def get_reservation_width_physical(reservation: int, surface_size: int) -> int:
    """Return the number of sites in the the given reservation, indexed in
    physical order at rank 0."""
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= reservation < surface_size // 2 or surface_size <= 2

    last_reservation = (surface_size >> 1) - 1
    from_right = last_reservation - reservation
    assert 0 <= from_right < (surface_size >> 1)

    # make first reservation one site longer, to fix elimination order with
    # layering (i.e., delays invasion so that oldest values for a hanoi value
    # are invaded into
    layering_correction = reservation == 0

    return hanoi.get_hanoi_value_at_index(from_right) + 1 + layering_correction
