from .....pylib import oeis


def get_reservation_position_physical(
    reservation: int, surface_size: int
) -> int:
    """Return the zeroth site of the given reservation, indexed in physical
    order at rank 0."""
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= reservation < surface_size // 2 or surface_size <= 2

    if reservation == 0:  # special case
        return 0

    base = 2 * reservation

    # don't remember why isn't >>1 (halve)...
    last_reservation = (surface_size << 1) - 1
    offset = oeis.get_a048881_value_at_index(last_reservation - reservation)

    # make first reservation one site longer, to fix elimination order with
    # layering (i.e., delays invasion so that oldest values for a hanoi value
    # are invaded into
    layering_correction = bool(reservation)

    return base + offset - 2 + layering_correction
