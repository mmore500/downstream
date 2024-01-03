from .....pylib.hanoi import (
    get_hanoi_value_at_index,
    get_hanoi_value_incidence_at_index,
)
from .._impl import get_nth_bin_position, get_nth_bin_width


def pick_deposition_site(rank: int, surface_size: int) -> int:
    assert surface_size.bit_count() == 1  # assume power of 2 surface size

    hanoi_value = get_hanoi_value_at_index(rank)
    hanoi_incidence = get_hanoi_value_incidence_at_index(rank)

    bin_index = hanoi_incidence  # zero indexed
    num_available_bins = surface_size // 2
    if bin_index >= num_available_bins:
        return 0  # TODO
    else:
        bin_width = get_nth_bin_width(bin_index, surface_size)
        within_bin_position = hanoi_value % bin_width

        bin_position = get_nth_bin_position(bin_index, surface_size)

        res = 1 + bin_position + within_bin_position  # index 0 reserved
        assert 1 <= res < surface_size
        return res
