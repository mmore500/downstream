import typing

from ..tilted_algo import (
    calc_resident_deposition_rank as impl_calc_resident_deposition_rank,
)
from ._pick_deposition_site import pick_deposition_site


def calc_resident_deposition_rank(
    site: int,
    surface_size: int,
    num_depositions: int,
    grip: typing.Optional[int] = None,
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at site `site`?

    "grip" stands for genesis reservation index physical of a site. This
    argument may be passed optionally, as an optimization --- i.e., when
    calling via `iter_resident_deposition_ranks`.

    Somewhat (conceptually) inverse to `pick_deposition_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.
    """
    assert surface_size.bit_count() == 1

    if num_depositions == 0:
        return 0
    rank = num_depositions - 1

    if site == 0:
        return 0

    last_site = pick_deposition_site(rank, surface_size)
    if site == last_site:
        return rank

    return impl_calc_resident_deposition_rank(
        site, surface_size, num_depositions, grip=grip
    )
