from .....pylib import hanoi, oeis


def get_global_epoch(rank: int, surface_size: int) -> int:
    """Return the reservation-halving epoch of the given rank.

    Rank zero is at 0th epoch. Epochs count up with each reservation count
    halving.
    """
    assert surface_size.bit_count() == 1  # power of 2
    max_hanoi = hanoi.get_max_hanoi_value_through_index(rank)
    base_hanoi = surface_size.bit_length() - 1
    if max_hanoi < base_hanoi:
        return 0
    else:
        assert max_hanoi - base_hanoi >= 0
        return min(
            oeis.get_a000295_index_of_value(max_hanoi - base_hanoi) + 1,
            surface_size.bit_length() - 2,
        )
