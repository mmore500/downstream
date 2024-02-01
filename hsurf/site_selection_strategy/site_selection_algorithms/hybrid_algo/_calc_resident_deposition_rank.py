from ..steady_algo import calc_resident_deposition_rank as steady_impl
from ..tilted_algo import calc_resident_deposition_rank as tilted_impl


def calc_resident_deposition_rank(
    site: int,
    surface_size: int,
    num_depositions: int,
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

    if site < (surface_size >> 1):
        num_depositions += 1
        res = steady_impl(site, surface_size >> 1, num_depositions >> 1)
        return res << 1
    else:
        site -= surface_size >> 1
        res = tilted_impl(site, surface_size >> 1, num_depositions >> 1)
        correction = bool(res) | (site == 0 and num_depositions >= 2)
        return (res << 1) + correction
