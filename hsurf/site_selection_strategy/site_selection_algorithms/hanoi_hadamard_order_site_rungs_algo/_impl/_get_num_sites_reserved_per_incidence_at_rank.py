from ..... import pylib


def get_num_sites_reserved_per_incidence_at_rank(rank: int) -> int:
    return pylib.bit_ceil(
        pylib.hanoi.get_max_hanoi_value_through_index(rank) + 1
    )
