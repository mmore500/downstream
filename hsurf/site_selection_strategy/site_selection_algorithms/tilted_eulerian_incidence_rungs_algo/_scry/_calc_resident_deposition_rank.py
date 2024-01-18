from .....pylib import hanoi, fast_pow2_mod
from .._impl import (
    calc_hanoi_invasion_rank,
    calc_resident_hanoi_value,
    get_epoch_rank,
    get_global_epoch,
    get_global_num_reservations,
    get_hanoi_num_reservations,
    get_site_hanoi_value_assigned,
    get_site_reservation_index_logical,
    get_site_reservation_index_logical_at_epoch,
)


def calc_resident_deposition_rank(
    site: int,
    surface_size: int,
    num_depositions: int,
    _recursion_depth: int = 0,
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at site `site`?

    Somewhat (conceptually) inverse to `pick_deposition_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.
    """
    assert _recursion_depth < 2

    if num_depositions == 0:
        return 0
    rank = num_depositions - 1

    actual_hanoi_value = calc_resident_hanoi_value(
        site, surface_size, num_depositions
    )
    if actual_hanoi_value == get_site_hanoi_value_assigned(
        site, rank, surface_size
    ):
        return _calc_resident_rank_nonstale_case(
            site, rank, surface_size, actual_hanoi_value
        )
    elif actual_hanoi_value == 0 and rank < surface_size - 1:
        # not-yet-deposited-to case
        return 0
    else:
        return _calc_resident_rank_stale_case(
            site, rank, surface_size, actual_hanoi_value, _recursion_depth
        )


def _calc_rank_from_incidence(
    hanoi_value: int,
    reservation: int,
    num_reservations: int,
    rank: int,
) -> int:
    """Calculate the rank of a site based on the incidence of the hanoi value
    located there."""
    assert reservation < num_reservations

    incidence_seen = (
        hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value, rank
        )
        - 1
    )
    assert incidence_seen >= 0

    if incidence_seen < reservation:
        return 0

    site_incidence = (
        incidence_seen
        - fast_pow2_mod(incidence_seen, num_reservations)
        + reservation
    )
    if site_incidence > incidence_seen:
        site_incidence -= num_reservations
    assert 0 <= site_incidence
    assert site_incidence <= incidence_seen
    res = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value, site_incidence
    )
    assert 0 <= res <= rank
    return res


def _get_epoch_rank(hanoi_value, rank, surface_size):
    """Get rank of previous epoch, taking invasion of focal hanoi value
    also as an epoch transition."""
    epoch = get_global_epoch(rank, surface_size)
    epoch_rank = get_epoch_rank(epoch, surface_size)
    assert epoch_rank <= rank

    if epoch:
        invasion_rank = calc_hanoi_invasion_rank(
            hanoi_value, epoch, surface_size
        )
        if invasion_rank <= rank:
            epoch_rank = invasion_rank
    return epoch_rank


def _get_cur_epoch_hanoi_count(
    hanoi_value: int, rank: int, surface_size: int
) -> int:
    """How many instances of the focal hanoi value have been deposited during
    the current epoch?"""
    epoch_rank = _get_epoch_rank(hanoi_value, rank, surface_size)
    res = hanoi.get_incidence_count_of_hanoi_value_through_index(
        hanoi_value, rank
    ) - hanoi.get_incidence_count_of_hanoi_value_through_index(
        hanoi_value, epoch_rank
    )
    assert res >= 0
    return res


def _calc_resident_rank_nonstale_case(
    site: int, rank: int, surface_size: int, hanoi_value: int
) -> int:
    """Implementation detial for case where ranks with this epoch's hanoi value
    are in place at site."""
    reservation = get_site_reservation_index_logical(site, rank, surface_size)
    num_reservations = get_hanoi_num_reservations(
        rank, surface_size, hanoi_value
    )
    assert reservation < num_reservations
    naive_rank = _calc_rank_from_incidence(
        hanoi_value, reservation, num_reservations, rank
    )

    cehc = _get_cur_epoch_hanoi_count(hanoi_value, rank, surface_size)
    if cehc > reservation:
        return naive_rank

    prev_epoch_rank = _get_epoch_rank(hanoi_value, rank, surface_size) - 1
    if prev_epoch_rank >= 0:
        num_reservations = get_hanoi_num_reservations(
            prev_epoch_rank, surface_size, hanoi_value
        )
        return _calc_rank_from_incidence(
            hanoi_value, reservation, num_reservations, rank
        )

    return naive_rank


def _calc_resident_rank_stale_case(
    site: int,
    rank: int,
    surface_size: int,
    hanoi_value: int,
    _recursion_depth: int,  # just for debugging
) -> int:
    """Implementation detial for case where ranks with this epoch's hanoi value
    are not yet in place at site."""
    assert _recursion_depth < 2

    # if invaded, go back to right before invasion
    epoch = get_global_epoch(rank, surface_size)
    invasion_rank = calc_hanoi_invasion_rank(hanoi_value, epoch, surface_size)
    if invasion_rank <= rank:
        return calc_resident_deposition_rank(
            site,
            surface_size,
            invasion_rank,  # +1/-1 cancel out
            _recursion_depth + 1,
        )

    reservation = get_site_reservation_index_logical(site, rank, surface_size)
    cehc = _get_cur_epoch_hanoi_count(hanoi_value, rank, surface_size)
    if cehc <= reservation:
        assert epoch
        return calc_resident_deposition_rank(
            site,
            surface_size,
            get_epoch_rank(epoch, surface_size),  # +1/-1 cancel out
            _recursion_depth + 1,
        )

    assert epoch
    num_reservations = 2 * get_global_num_reservations(rank, surface_size)
    reservation = get_site_reservation_index_logical_at_epoch(
        site, epoch - 1, surface_size
    )

    assert reservation < num_reservations
    return _calc_rank_from_incidence(
        hanoi_value, reservation, num_reservations, rank
    )
