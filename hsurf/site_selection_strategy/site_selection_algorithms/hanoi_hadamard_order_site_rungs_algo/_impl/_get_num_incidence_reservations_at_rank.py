from ._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)


def get_num_incidence_reservations_at_rank(
    rank: int, surface_size: int
) -> int:
    reservation_size = get_num_sites_reserved_per_incidence_at_rank(rank)
    assert surface_size % reservation_size == 0
    num_reservations = surface_size // reservation_size
    return num_reservations