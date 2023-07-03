import opytional as opyt

from ._impl import (
    calc_rank_of_deposited_hanoi_value,
    calc_resident_hanoi_context,
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
    resident_hanoi_context = calc_resident_hanoi_context(
        site, surface_size, num_depositions
    )
    # candidate_hanoi_value is the hanoi value associated with the
    # deposition resident at site
    # ... use this information to deduce the rank at which the resident
    # deposition at site was deposited
    res = opyt.apply_if_or_value(
        resident_hanoi_context,
        lambda context: calc_rank_of_deposited_hanoi_value(
            context["hanoi value"],
            context["reservation index"],
            surface_size,
            context["focal rank"],
        ),
        0,  # fallback value: no algorithm deposition at site yet
    )
    if num_depositions:
        assert res < num_depositions
    else:
        assert res == 0
    return res
