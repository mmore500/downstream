import typing

import interval_search as inch

from ......pylib import bit_floor, fast_pow2_divide, hanoi
from ..._impl._get_num_reservations_provided import (
    get_num_reservations_provided,
)
from ..._impl._get_surface_rank_capacity import get_surface_rank_capacity


def get_reservation_index_elimination_rank(
    hanoi_value: int,
    reservation_index: int,
    surface_size: int,
) -> typing.Optional[int]:
    # note: this function signature could be simplified by returning 0 instead
    # for the None case because non-None values are always nonzero
    """Find the rank `r` where `hanoi_value`'s incidence reservation buffer
    size transitions from having space to hold a `reservation_index` position
    to having size less than or equal to `reservation_index`.

    Used to determine the very last possible rank where `hanoi_value` could be
    deposited at a site. (This is the rank before the elimination rank.)
    """

    first_incidence_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value, 0
    )
    max_reservations_provided = get_num_reservations_provided(
        hanoi_value=hanoi_value,
        surface_size=surface_size,
        rank=first_incidence_rank,
    )
    if reservation_index == 0:
        # special case
        # honor implicit assumption that rank cap is respected, so there will
        # always be at least one reservation index per hanoi value
        res = get_surface_rank_capacity(surface_size) - 1
        assert res
        return res
    elif reservation_index >= max_reservations_provided:
        # reservation_index is out of bounds of the largest-possible incidence
        # reservation buffer that ever provided for hanoi_value (i.e., the
        # incidence reservation buffer size provided at the first deposition of
        # hanoi_value)
        # so, this reservation index is never eliminated because it never
        # exists
        return None
    else:
        # do solve for elimination rank: binary search the first rank where num
        # reservations provided would be insufficient to contain
        # reservation_index
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
        upper_bound_exclusive = get_surface_rank_capacity(surface_size)
        upper_bound_inclusive = upper_bound_exclusive - 1
        assert predicate(upper_bound_inclusive)

        # precaculations for ansatz
        # how many reservations will be left when this cycle concludes?
        remaining_reservations = bit_floor(reservation_index)

        inv_remaining_index = reservation_index - remaining_reservations
        assert 0 <= inv_remaining_index < remaining_reservations

        # how many index steps into this cycle will reservation index get
        # eliminated?
        # remember that reservations are eliminated back to front
        remaining_index = remaining_reservations - inv_remaining_index - 1
        assert 0 <= remaining_index < remaining_reservations

        hanoi_invader = (
            fast_pow2_divide(
                surface_size,
                2 * remaining_reservations,
            )
            + hanoi_value
        )
        assert hanoi_invader > hanoi_value

        # ansatz will serve as upper bound
        # might to be able to eliminate binary search
        # by calculating downgrade rank associated with ansztz
        # (started in get_downgrade_rank_naive)
        ansatz = hanoi.get_index_of_hanoi_value_nth_incidence(
            hanoi_invader, remaining_index
        )
        assert ansatz <= upper_bound_inclusive
        assert predicate(ansatz)

        lower_bound = hanoi.get_index_of_hanoi_value_nth_incidence(
            hanoi_value, 0
        )
        assert lower_bound >= 0
        # note that this existing lower bound is broken due to #5
        # so, use most conservative lower bound
        # also, not very confident in this lower bound above, needs testing
        lower_bound = first_incidence_rank
        assert not predicate(lower_bound)

        res = inch.binary_search(predicate, lower_bound, ansatz)
        assert res
        assert res < upper_bound_exclusive
        return res
