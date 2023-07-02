from .....pylib import hanoi
from .._impl import get_num_reservations_provided
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

    candidate_zip = zip(
        iter_candidate_hanoi_occupants(site, rank),
        iter_candidate_reservation_indices(site, surface_size, rank),
    )
    for candidate_hanoi_value, candidate_reservation_index in candidate_zip:
        deadline_rank = get_reservation_index_elimination_rank(
            candidate_hanoi_value,
            candidate_reservation_index,
            surface_size,
        )
        if deadline_rank is None:
            assert all(
                get_reservation_index_elimination_rank(
                    candidate_hanoi_value_,
                    candidate_reservation_index_,
                    surface_size,
                )
                is None
                and (
                    candidate_hanoi_value_ / candidate_reservation_index_
                    <= candidate_hanoi_value / candidate_reservation_index
                )
                for (
                    candidate_hanoi_value_,
                    candidate_reservation_index_,
                ) in candidate_zip
                if candidate_hanoi_value_ > 0
            ), {
                "candidate_hanoi_value": candidate_hanoi_value,
                "candidate_reservation_index": candidate_reservation_index,
                "max_num_reservations_provided": get_num_reservations_provided(
                    0, surface_size, 0
                ),
                "surface_size": surface_size,
                "rank": rank,
                "site": site,
            }
            break  # continue also works here

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
