from .....pylib import bit_ceil, fast_pow2_mod, hanoi
from .....pylib import longevity_ordering_descending as hadamard_order
from .._impl import get_num_reservations_provided, get_surface_rank_capacity


def pick_deposition_site(rank: int, surface_size: int) -> int:
    if rank > get_surface_rank_capacity(surface_size):
        raise ValueError(
            f"{surface_size}-bit surface only valid "
            "through rank <= {get_surface_rank_capacity(surface_size)}, "
            f"rank {rank} was requested"
        )

    within_reservation_offset = hanoi.get_hanoi_value_at_index(rank)

    num_incidence_reservations = get_num_reservations_provided(
        within_reservation_offset, surface_size, rank
    )

    reservation_index = (
        hanoi.get_hanoi_value_incidence_at_index(rank)
        % num_incidence_reservations
    )

    longevity_ordered_reservation_position = (
        # this is more correct in a theoretical sense, and does have some effect
        # but actual functional improvements relative to simpler naive/alternating
        # should be tested; it may not be worth the extra complexity
        hadamard_order.get_longevity_mapped_position_of_index(
            reservation_index,
            surface_size,
        )
    )
    if reservation_index == 0:
        assert longevity_ordered_reservation_position == 0
    elif reservation_index == bit_ceil(num_incidence_reservations) - 1:
        assert longevity_ordered_reservation_position == (
            surface_size // bit_ceil(num_incidence_reservations)
        )

    res = longevity_ordered_reservation_position + within_reservation_offset
    if rank == 0:
        assert res == 0, {
            "longevity_ordered_reservation_position": longevity_ordered_reservation_position,
            "reservation_index": reservation_index,
            "surface_size": surface_size,
            "within_reservation_offset": within_reservation_offset,
        }
    assert res < surface_size
    return res
