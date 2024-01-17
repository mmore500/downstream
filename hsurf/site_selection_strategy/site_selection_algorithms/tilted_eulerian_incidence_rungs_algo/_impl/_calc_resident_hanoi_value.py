from .....pylib import hanoi, fast_pow2_mod
from ._get_epoch_rank import get_epoch_rank
from ._get_global_epoch import get_global_epoch
from ._get_global_num_reservations import get_global_num_reservations
from ._get_site_hanoi_value_assigned import get_site_hanoi_value_assigned
from ._get_site_reservation_index_logical import (
    get_site_reservation_index_logical,
)


def calc_resident_hanoi_value(
    site: int,
    surface_size: int,
    num_depositions: int,
    _recursion_depth: int = 0,  # only for debugging/validation
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    hanoi value of the stratum resident at site `site`?

    Implementation detail for `calc_resident_deposition_rank`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.
    """

    assert _recursion_depth <= 1  # should recurse at most once

    if num_depositions == 0:
        return 0
    rank = num_depositions - 1
    epoch = get_global_epoch(rank, surface_size)
    epoch_rank = get_epoch_rank(epoch, surface_size)

    num_reservations = get_global_num_reservations(rank, surface_size)
    reservation = get_site_reservation_index_logical(site, rank, surface_size)
    ansatz_hanoi = get_site_hanoi_value_assigned(site, rank, surface_size)
    num_seen = hanoi.get_incidence_count_of_hanoi_value_through_index(
        ansatz_hanoi, rank
    )

    epoch_incidence_count = (
        hanoi.get_incidence_count_of_hanoi_value_through_index(
            ansatz_hanoi, epoch_rank - 1
        )
        if epoch_rank  # special-case zeroth epoch
        else 0
    )
    num_seen_this_epoch = num_seen - epoch_incidence_count
    epoch_offset = fast_pow2_mod(epoch_incidence_count, num_reservations)

    assert num_seen_this_epoch >= 0

    if reservation >= epoch_offset + num_seen_this_epoch:
        # handle case where the assigned hanoi value has not yet been deposited
        return (
            calc_resident_hanoi_value(
                site,
                surface_size,
                epoch_rank,
                _recursion_depth=_recursion_depth + 1,
            )
            if epoch_rank  # special-case zeroth epoch
            else 0
        )

    return ansatz_hanoi
