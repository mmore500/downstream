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
    reservation = fast_pow2_mod(-incidence - 1, num_reservations)
    hanoi_value = hanoi.get_hanoi_value_at_index(rank)
    res = (
        get_reservation_position_logical(reservation, surface_size)
        + hanoi_value
    )
    assert 0 <= res < surface_size
    return res
