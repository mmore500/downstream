from .....pylib.hanoi import (
    get_index_of_hanoi_value_nth_incidence,
    get_min_hanoi_value_with_incidence_at_least,
)
from .._enact import pick_deposition_site
from .._impl import (
    get_bin_number_of_position,
    get_nth_bin_position,
    get_nth_bin_width,
    get_num_bins,
)


def calc_resident_deposition_rank(
    site: int, surface_size: int, num_depositions: int
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at site `site`?

    Somewhat (conceptually) inverse to `pick_deposition_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.
    """
    # handle chaff
    if site == pick_deposition_site(num_depositions - 1, surface_size):
        return num_depositions - 1

    if site == 0:  # handle special-cased position zero
        return 0
    site -= 1  # handle special-cased position zero

    bin_number = get_bin_number_of_position(site, surface_size)
    bin_width = get_nth_bin_width(bin_number, surface_size)
    within_bin_index = site - get_nth_bin_position(bin_number, surface_size)
    assert 0 <= within_bin_index < bin_width

    most_recent_bin_invader_hanoi_value = (
        get_min_hanoi_value_with_incidence_at_least(
            bin_number, num_depositions - 2  # -1 for special case 0 offset
        )
    )
    if most_recent_bin_invader_hanoi_value is None:
        return 0

    _most_recent_bin_invader_hanoi_value_bin_index = (
        most_recent_bin_invader_hanoi_value % bin_width
    )
    _most_recent_bin_root_invader_hanoi_value = (
        most_recent_bin_invader_hanoi_value
        - _most_recent_bin_invader_hanoi_value_bin_index
    )
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
    assert 0 <= bin_number < get_num_bins(surface_size)
    res = (
        get_index_of_hanoi_value_nth_incidence(
            most_recent_site_invader_hanoi_value, bin_number
        )
        + 1
    )  # +1 adds offset for special-casing of zeroth entry
    assert 1 <= res < num_depositions
    return res
