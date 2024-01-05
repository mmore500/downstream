from .....pylib.hanoi import (
    get_index_of_hanoi_value_nth_incidence,
    get_min_hanoi_value_with_incidence_at_least,
)
from ._get_nth_bin_width import get_nth_bin_width
from ._get_num_bins import get_num_bins


def calc_resident_deposition_rank_wrt_bin(
    bin_number: int,
    within_bin_index: int,
    num_depositions: int,
    _surface_size: int,  # only for assertions
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at site `site`?

    Somewhat (conceptually) inverse to `pick_deposition_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.

    Implementation detail for scry algorithms.
    """
    if num_depositions == 0:
        return 0

    bin_width = get_nth_bin_width(bin_number, _surface_size)
    assert 0 <= within_bin_index < bin_width

    most_recent_bin_invader_hanoi_value = (
        get_min_hanoi_value_with_incidence_at_least(
            bin_number, num_depositions - 1
        )
    )
    if most_recent_bin_invader_hanoi_value is None:
        return 0

    _most_recent_bin_invader_hanoi_value_bin_index = (
        most_recent_bin_invader_hanoi_value % bin_width
    )  # for assertions
    _most_recent_bin_root_invader_hanoi_value = (
        most_recent_bin_invader_hanoi_value
        - _most_recent_bin_invader_hanoi_value_bin_index
    )  # for assertions
    assert (
        _most_recent_bin_root_invader_hanoi_value
        <= most_recent_bin_invader_hanoi_value
    )
    assert (
        most_recent_bin_invader_hanoi_value
        - _most_recent_bin_root_invader_hanoi_value
        < bin_width
    )
    most_recent_site_invader_hanoi_value = (
        (most_recent_bin_invader_hanoi_value - within_bin_index)
        - (most_recent_bin_invader_hanoi_value - within_bin_index) % bin_width
    ) + within_bin_index
    if most_recent_site_invader_hanoi_value < 0:
        return 0
    assert (
        most_recent_bin_invader_hanoi_value - bin_width
        < _most_recent_bin_root_invader_hanoi_value
        <= most_recent_bin_invader_hanoi_value
    )
    assert most_recent_site_invader_hanoi_value % bin_width == within_bin_index
    assert (
        most_recent_site_invader_hanoi_value
        <= most_recent_bin_invader_hanoi_value
    )
    assert 0 <= bin_number < get_num_bins(_surface_size)
    res = get_index_of_hanoi_value_nth_incidence(
        most_recent_site_invader_hanoi_value, bin_number
    )
    assert 0 <= res < num_depositions
    return res
