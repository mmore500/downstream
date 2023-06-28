import typing

import interval_search as inch

from ......pylib import hanoi
from ..._impl._get_num_reservations_provided import (
    get_num_reservations_provided,
)
from ..._impl._get_surface_rank_capacity import get_surface_rank_capacity


def get_reservation_index_elimination_rank(
    hanoi_value: int,
    reservation_index: int,
    surface_size: int,
) -> typing.Optional[int]:

    first_incidence_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value, 0
    )
    max_reservations_provided = get_num_reservations_provided(
        hanoi_value=hanoi_value,
        surface_size=surface_size,
        rank=first_incidence_rank,
    )
    if reservation_index == 0:
        # special case because we implicitly assume
        # always at least one reservation index
        res = get_surface_rank_capacity(surface_size) - 1
        assert res
        return res
    elif reservation_index >= max_reservations_provided:
        return None
    else:

        def predicate(rank: int) -> bool:
            return (
                get_num_reservations_provided(
                    hanoi_value=hanoi_value,
                    surface_size=surface_size,
                    rank=rank,
                )
                <= reservation_index
            )

        assert not predicate(0)
        upper_bound = get_surface_rank_capacity(surface_size) - 1
        assert predicate(upper_bound)
        res = inch.binary_search(
            predicate,
            first_incidence_rank,
            # upper bound prevents assertion errors from out of bounds queries
            upper_bound,
        )
        assert res, {
            "first_incidence_rank": first_incidence_rank,
            "max_reservations_provided": max_reservations_provided,
            "res": res,
            "reservation_index": reservation_index,
            "surface_size": surface_size,
            "upper_bound": upper_bound,
        }
        return res
