from .....pylib import fast_pow2_divide, hanoi
from ._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)
from ._is_hanoi_invaded import is_hanoi_invaded
from ._is_hanoi_invader import is_hanoi_invader


def get_upcoming_hanoi_invasion_value(hanoi_value: int, rank: int) -> int:
    """What hanoi value will next invade sites associated with `hanoi_value`?

    If any reservation sites associated with `hanoi_value` at the outset of the
    current reservation-size-doubling cycle have been overwritten by another
    hanoi value (e.g., an invasion has already begun), the invading hanoi value
    associated with the _next_ cycle will be returned. Otherwise, if the
    current-cycle invasion has not begun the current-cycle invading hanoi value
    will be returned.
    """
    rank = max(
        rank,
        hanoi.get_index_of_hanoi_value_nth_incidence(hanoi_value, 0),
    )

    reservation_width = get_num_sites_reserved_per_incidence_at_rank(rank)
    if is_hanoi_invader(hanoi_value, rank) or is_hanoi_invaded(
        hanoi_value, rank
    ):
        return hanoi_value + reservation_width
    else:
        return hanoi_value + fast_pow2_divide(reservation_width, 2)
