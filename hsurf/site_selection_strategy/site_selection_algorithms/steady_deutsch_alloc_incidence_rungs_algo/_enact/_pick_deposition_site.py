from .....pylib import fast_pow2_mod
from .....pylib.hanoi import (
    get_hanoi_value_at_index,
    get_hanoi_value_incidence_at_index,
    get_incidence_count_of_hanoi_value_through_index,
    get_max_hanoi_value_through_index,
    get_hanoi_value_index_offset,
    get_index_of_hanoi_value_next_incidence,
)
from .._impl import get_nth_bin_position, get_nth_bin_width


def pick_deposition_site(
    rank: int, surface_size: int, _recursion_depth: bool = 0
) -> int:
    assert surface_size.bit_count() == 1  # assume power of 2 surface size

    if rank == 0:  # handle permanent deposition into site zero as special case
        return 0
    rank -= 1

    hanoi_value = get_hanoi_value_at_index(rank)
    hanoi_incidence = get_hanoi_value_incidence_at_index(rank)

    bin_index = hanoi_incidence  # zero indexed
    num_available_bins = surface_size // 2
    if bin_index >= num_available_bins:
        assert _recursion_depth < 1  # only expect one-deep recursion
        longest_bin_width = get_nth_bin_width(0, surface_size)
        largest_active_hanoi = get_max_hanoi_value_through_index(rank)
        assert largest_active_hanoi > hanoi_value
        assert largest_active_hanoi >= longest_bin_width
        smallest_active_hanoi = largest_active_hanoi - longest_bin_width + 1
        smallest_active_hanoi += (
            get_incidence_count_of_hanoi_value_through_index(
                smallest_active_hanoi, rank
            )
            >= num_available_bins
        )  # correction factor, if needed
        assert (
            get_incidence_count_of_hanoi_value_through_index(
                smallest_active_hanoi, rank
            )
            < num_available_bins
        )  # check is active
        assert (
            get_incidence_count_of_hanoi_value_through_index(
                smallest_active_hanoi - 1, rank
            )
            >= num_available_bins
        )  # check is smallest active --- smaller are inactive
        smallest_active_hanoi_rank = get_index_of_hanoi_value_next_incidence(
            smallest_active_hanoi,
            rank,
        )
        next_active_rank = smallest_active_hanoi_rank

        active_cadence = get_hanoi_value_index_offset(smallest_active_hanoi) + 1
        assert active_cadence.bit_count() == 1  # expect power of 2
        if next_active_rank - rank > active_cadence:
            next_active_rank -= active_cadence

        assert rank < next_active_rank < rank + active_cadence
        assert (
            get_hanoi_value_at_index(next_active_rank) >= smallest_active_hanoi
        )
        return pick_deposition_site(
            next_active_rank + 1,  # undo shift down by one
            surface_size=surface_size,
            _recursion_depth=_recursion_depth + 1,
        )
    else:
        bin_width = get_nth_bin_width(bin_index, surface_size)
        within_bin_position = hanoi_value % bin_width

        bin_position = get_nth_bin_position(bin_index, surface_size)

        res = 1 + bin_position + within_bin_position  # index 0 reserved
        assert 1 <= res < surface_size
        return res
