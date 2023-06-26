from .....pylib import hanoi
from ._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)
from ._is_hanoi_invader import is_hanoi_invader


def is_hanoi_invaded(hanoi_value: int, rank: int) -> bool:
    reservation_width = get_num_sites_reserved_per_incidence_at_rank(rank)
    max_hanoi_value = hanoi.get_max_hanoi_value_through_index(rank)

    return (
        not is_hanoi_invader(hanoi_value, rank)
        and max_hanoi_value >= hanoi_value + reservation_width // 2
    )
