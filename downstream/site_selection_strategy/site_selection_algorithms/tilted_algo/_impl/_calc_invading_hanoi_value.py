from .....pylib import oeis


def calc_invading_hanoi_value(
    hanoi_value: int, epoch: int, surface_size: int
) -> int:
    """At the first incidence of what hanoi value will the reservation
    be shrunk?"""
    assert epoch > 0  # no invasions in zeroth epoch
    assert surface_size.bit_count() == 1  # power of 2

    base_hanoi = surface_size.bit_length() - 1
    reservation0_begin = base_hanoi + oeis.get_a000295_value_at_index(
        epoch - 1
    )

    return reservation0_begin + hanoi_value
