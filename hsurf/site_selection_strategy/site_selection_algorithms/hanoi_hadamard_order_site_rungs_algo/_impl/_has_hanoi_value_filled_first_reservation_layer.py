from .....pylib import hanoi
from ._get_num_incidence_reservations_at_rank import (
    get_num_incidence_reservations_at_rank,
)
from ._get_surface_rank_capacity import get_surface_rank_capacity


def has_hanoi_value_filled_first_reservation_layer(
    hanoi_value: int, surface_size: int, rank: int
) -> bool:
    """Are the number of incidences of hanoi value elapsed by rank `rank`
    greater than or equal to the number of incidence reservation buffer
    positions available at the time point when hanoi value's first incidence
    occured?"""
    first_instance_index = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value, 0
    )
    if first_instance_index >= get_surface_rank_capacity(surface_size):
        return False

    first_layer_size = get_num_incidence_reservations_at_rank(
        hanoi.get_index_of_hanoi_value_nth_incidence(hanoi_value, 0),
        surface_size,
    )
    return not (
        hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value,
            rank,
        )
        < first_layer_size
    )
