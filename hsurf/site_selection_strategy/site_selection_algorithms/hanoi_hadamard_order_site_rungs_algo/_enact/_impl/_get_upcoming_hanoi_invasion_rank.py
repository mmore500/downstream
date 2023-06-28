from ......pylib import hanoi
from ._get_upcoming_hanoi_invasion_value import (
    get_upcoming_hanoi_invasion_value,
)


def get_upcoming_hanoi_invasion_rank(hanoi_value: int, rank: int) -> int:
    upcoming_invasion_hanoi_value = get_upcoming_hanoi_invasion_value(
        hanoi_value, rank
    )
    upcoming_invasion_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
        upcoming_invasion_hanoi_value, 0
    )

    return upcoming_invasion_rank
