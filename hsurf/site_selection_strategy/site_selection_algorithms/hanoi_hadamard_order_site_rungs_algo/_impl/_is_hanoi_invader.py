from ._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)


def is_hanoi_invader(hanoi_value: int, rank: int) -> bool:
    reservation_width = get_num_sites_reserved_per_incidence_at_rank(rank)
    return hanoi_value >= reservation_width // 2
