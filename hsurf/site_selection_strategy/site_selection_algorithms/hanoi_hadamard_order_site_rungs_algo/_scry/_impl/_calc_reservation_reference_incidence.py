from ......pylib import hanoi
from ..._impl._get_num_reservations_provided import (
    get_num_reservations_provided,
)


def calc_reservation_reference_incidence(
    hanoi_value: int,
    reservation_index: int,
    surface_size: int,
    focal_rank: int,
) -> int:
    """What is the most recent hanoi value incidence preceding the deposition
    at the `reservation_index`'th incidence reservation ring buffer position to
    align to the zeroth incidence reservation ring buffer position?

    Parameters
    ----------
    hanoi_value : int
        The hanoi value of the focal incidence reservation ring buffer.
    reservation_index : int
        The semantic position (i.e., before being mapped through the longevity
        ordering) in the ring buffer for which to find the preceding zero-
        buffer-site-aligned hanoi value incidence.
    surface_size : int
        Number of sites on surface. A power of 2 is assumed.
    focal_rank : int
        Zero-indexed deposition count (across all hanoi values) on the surface
        at the current point in time.

    Returns
    -------
    int
        The number of `hanoi_value` depositions that occured prior to the
        deposition of the stratum at `reservation_index`.
    """
    num_reservations_provided = get_num_reservations_provided(
        hanoi_value=hanoi_value,
        surface_size=surface_size,
        rank=focal_rank,
    )
    assert num_reservations_provided
    assert reservation_index < num_reservations_provided, {
        "hanoi_value": hanoi_value,
        "reservation_index": reservation_index,
        "surface_size": surface_size,
        "focal_rank": focal_rank,
        "num_reservations_provided": num_reservations_provided,
    }

    num_incidences = hanoi.get_incidence_count_of_hanoi_value_through_index(
        hanoi_value, focal_rank
    )
    assert num_incidences
    hanoi_incidence = num_incidences - 1
    assert (
        hanoi.get_index_of_hanoi_value_nth_incidence(
            hanoi_value, hanoi_incidence
        )
        <= focal_rank
    )

    # incidence position is the clock face value for the hanoi value incidence
    # most recent to the focal rank
    incidence_position = hanoi_incidence % num_reservations_provided
    # subtract off remainder to get zero-aligned incidence preceding focal rank
    candidate_incidence = hanoi_incidence - incidence_position

    # should we accept candidate incidence?
    # if the reservation index is PAST the most recent incidence position,
    # that means that it's actually left over from the last cycle around the
    # clock face and occured PRIOR to the candidate incidence
    # so the candidate incidence is invalid as the reference incidence...
    if reservation_index > incidence_position:
        # ... in that case, we need to step back to the preceding zero-aligned
        # incidence. Note that we can't just subtract away one cycle length due
        # to the possibility of change in the cycle length

        # start by getting the time point associated with the current zero-
        # aligned candidate incidence...
        candidate_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
            hanoi_value,
            candidate_incidence,
        )
        assert candidate_rank  # because we're subtracting one below
        # ... and then calculate the reference incidence for the immediately
        # preceding timepoint, which will take us to the preceding reference
        # incidence
        # note: at most one recursive call occurs
        return calc_reservation_reference_incidence(
            hanoi_value,
            reservation_index,
            surface_size,
            candidate_rank - 1,
        )
    else:
        assert candidate_incidence % num_reservations_provided == 0, {
            "candidate_incidence": candidate_incidence,
            "num_reservations_provided": num_reservations_provided,
        }
        return candidate_incidence
