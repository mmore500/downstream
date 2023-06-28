from ......pylib import hanoi


def get_surface_rank_capacity(surface_size: int) -> int:
    return hanoi.get_index_of_hanoi_value_nth_incidence(surface_size, 0)
