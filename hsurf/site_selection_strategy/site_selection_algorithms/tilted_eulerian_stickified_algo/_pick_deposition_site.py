from ..tilted_eulerian_incidence_rungs_algo import (
    pick_deposition_site as impl_pick_deposition_site,
)


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
    res = impl_pick_deposition_site(
        rank, surface_size
    ) or impl_pick_deposition_site(rank + 1, surface_size)

    assert 0 < res < surface_size
    return res
