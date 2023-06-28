from ......pylib import hanoi
from ._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)
from ._is_hanoi_invaded import is_hanoi_invaded
from ._is_hanoi_invader import is_hanoi_invader


def get_upcoming_hanoi_invasion_value(hanoi_value: int, rank: int) -> int:
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
        return hanoi_value + reservation_width // 2
