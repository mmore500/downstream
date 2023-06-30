from .....pylib import hanoi
from ._impl import (
    calc_rank_of_deposited_hanoi_value,
    get_reservation_index_elimination_rank,
    iter_candidate_hanoi_occupants,
    iter_candidate_reservation_indices,
)


def calc_resident_deposition_rank(
    site: int, surface_size: int, num_depositions: int
) -> int:

    if num_depositions == 0:
        return 0

    rank = num_depositions - 1

    for candidate_hanoi_value, candidate_reservation_index in zip(
        iter_candidate_hanoi_occupants(site, rank),
        iter_candidate_reservation_indices(site, surface_size, rank),
    ):
        deadline_rank = get_reservation_index_elimination_rank(
            candidate_hanoi_value,
            candidate_reservation_index,
            surface_size,
        )
        if deadline_rank is None:
            continue  # could this be a break?

        assert deadline_rank, {
            "candidate_hanoi_value": candidate_hanoi_value,
            "candidate_reservation_index": candidate_reservation_index,
            "rank": rank,
            "site": site,
            "surface_size": surface_size,
        }

        focal_rank = min(rank, deadline_rank - 1)
        assert focal_rank <= rank

        hanoi_count = hanoi.get_incidence_count_of_hanoi_value_through_index(
            candidate_hanoi_value,
            focal_rank,
        )
        if hanoi_count > candidate_reservation_index:
            res = calc_rank_of_deposited_hanoi_value(
                candidate_hanoi_value,
                candidate_reservation_index,
                surface_size,
                focal_rank,
            )
            assert res <= rank, {
                "candidate_hanoi_value": candidate_hanoi_value,
                "candidate_reservation_index": candidate_reservation_index,
                "deadline_rank": deadline_rank,
                "focal_rank": focal_rank,
                "hanoi_count": hanoi_count,
                "rank": rank,
                "res": res,
                "site": site,
                "surface_size": surface_size,
            }
            return res

    return 0
