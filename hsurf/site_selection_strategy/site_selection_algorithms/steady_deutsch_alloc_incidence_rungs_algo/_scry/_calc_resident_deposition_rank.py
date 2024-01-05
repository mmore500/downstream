from .._enact import pick_deposition_site
from .._impl import (
    calc_resident_deposition_rank_wrt_bin,
    get_bin_number_of_position,
    get_nth_bin_position,
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
    if num_depositions == 0:
        return 0

    # handle chaff, a.k.a., depositions placed onto the surface for expired
    # hanoi values using lookahead to next unexpired hanoi value
    if site == pick_deposition_site(num_depositions - 1, surface_size):
        return num_depositions - 1

    if site == 0:  # handle special-cased position zero
        return 0
    site -= 1  # handle special-cased position zero

    bin_number = get_bin_number_of_position(site, surface_size)
    within_bin_index = site - get_nth_bin_position(bin_number, surface_size)

    return calc_resident_deposition_rank_wrt_bin(
        bin_number, within_bin_index, num_depositions, surface_size
    )
