import itertools as it
import typing

from ._calc_resident_deposition_rank import calc_resident_deposition_rank
from .._impl import get_reservation_width_physical


def iter_resident_deposition_ranks(
    surface_size: int, num_depositions: int
) -> typing.Iterable[int]:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at each site?

    Yields deposition ranks in order of site index, from site 0 up to site
    `surface_size`. Returns 0 if the resident stratum traces back to original
    randomization of the surface prior to any algorithm-determined stratum
    depositions.

    Somewhat (conceptually) inverse to `pick_deposition_site`.
    """
    num_reservations = surface_size >> 1

    site_counter = it.count()
    for reservation in range(num_reservations):
        width = get_reservation_width_physical(reservation, surface_size)
        for site in it.islice(site_counter, width):
            yield calc_resident_deposition_rank(
                site, surface_size, num_depositions, grip=reservation
            )

    assert next(site_counter) == surface_size
