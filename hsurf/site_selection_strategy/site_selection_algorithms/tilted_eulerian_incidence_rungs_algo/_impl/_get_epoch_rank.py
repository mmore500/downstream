from .....pylib import hanoi, oeis


def get_epoch_rank(epoch: int, surface_size: int) -> int:
    """At what rank does the reservation-halving epoch `epoch` begin?"""
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= epoch <= surface_size.bit_length() - 2

    if epoch == 0:
        return 0

    base_hanoi = surface_size.bit_length() - 1
    offset = oeis.get_a000295_value_at_index(epoch - 1)
    max_hanoi = base_hanoi + offset

    return hanoi.get_hanoi_value_index_offset(max_hanoi)
