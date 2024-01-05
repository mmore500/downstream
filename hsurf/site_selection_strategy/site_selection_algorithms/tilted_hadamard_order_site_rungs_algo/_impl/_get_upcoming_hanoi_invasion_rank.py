from .....pylib import hanoi
from ._get_upcoming_hanoi_invasion_value import (
    get_upcoming_hanoi_invasion_value,
)


def get_upcoming_hanoi_invasion_rank(hanoi_value: int, rank: int) -> int:
    """At what rank will a hanoi invader of incidence reservation sites
    associated with `hanoi_value` next have a first (i.e., zeroth) incidence?

    See `get_upcoming_hanoi_invasion_value` for details.
    """
    upcoming_invasion_hanoi_value = get_upcoming_hanoi_invasion_value(
        hanoi_value, rank
    )
    upcoming_invasion_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
        upcoming_invasion_hanoi_value, 0
    )

    return upcoming_invasion_rank
