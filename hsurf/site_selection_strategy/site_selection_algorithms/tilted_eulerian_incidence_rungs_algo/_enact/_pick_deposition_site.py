from .....pylib import fast_pow2_mod, hanoi
from .._impl import (
    get_hanoi_num_reservations,
    get_reservation_position_logical,
)


def pick_deposition_site(
    rank: int,
    surface_size: int,
) -> int:
    """Pick the deposition site on a surface for a given rank.

    This function calculates a deposition site based on the rank and the surface size. It uses Hanoi tower algorithm and fast power of 2 modulo calculations to determine the specific site.

    Parameters
    ----------
    rank : int
        The number of time steps elapsed.
    surface_size : int
        The size of the surface on which deposition is to take place.

        Must be even power of two.

    Returns
    -------
    int
        Deposition site within surface..
    """
    num_reservations = get_hanoi_num_reservations(rank, surface_size)

    incidence = hanoi.get_hanoi_value_incidence_at_index(rank)
    hanoi_value = hanoi.get_hanoi_value_at_index(rank)
    hanoi0_correction = hanoi_value == 0
    # special correction for size 8 surface
    # necessary, but why?
    if surface_size == 8:
        hanoi1_correction = hanoi_value == 1
        # special case prevent overflow... simpler than tightening
        # get_hanoi_num_reservations
        hanoi1_correction *= -(rank == 5) or 1
    else:
        hanoi1_correction = 0
    reservation = fast_pow2_mod(
        incidence + hanoi0_correction + hanoi1_correction, num_reservations
    )
    res = (
        get_reservation_position_logical(reservation, surface_size)
        + hanoi_value
    )
    assert 0 <= res < surface_size - 1  # empty site at the end
    return res
