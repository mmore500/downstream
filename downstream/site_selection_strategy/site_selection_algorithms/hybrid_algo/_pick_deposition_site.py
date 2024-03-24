from ....pylib import fast_pow2_mod
from ..steady_algo import pick_deposition_site as steady_impl
from ..tilted_algo import pick_deposition_site as tilted_mpl


def pick_deposition_site(
    rank: int,
    surface_size: int,
) -> int:
    """Pick the deposition site on a surface for a given rank.

    This function calculates a deposition site based on the rank and the
    surface size.

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
        Deposition site within surface.
    """
    assert surface_size.bit_count() == 1

    if rank == 0:
        return 0
    if fast_pow2_mod(rank, 2) == 0:
        return steady_impl(rank >> 1, surface_size >> 1)
    else:
        return tilted_mpl(rank >> 1, surface_size >> 1) + (surface_size >> 1)
