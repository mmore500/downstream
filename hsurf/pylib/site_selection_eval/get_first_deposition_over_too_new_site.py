import typing

from ..hanoi import get_hanoi_value_at_index


def get_first_deposition_over_too_new_site(
    get_deposition_site_at_rank_impl: typing.Callable,
    get_num_reservations_provided_impl: typing.Callable,
    get_reservation_pos_impl: typing.Callable,
    surface_size: int,
    num_generations: int,
    progress_wrap: typing.Callable = lambda x: x,
) -> typing.Optional[typing.Dict]:

    surface_deposition_ranks = [-1] * surface_size
    surface_hanoi_values = [-1] * surface_size

    for generation in progress_wrap(range(num_generations)):
        target_site = get_deposition_site_at_rank_impl(
            generation, surface_size
        )
        hanoi_value = get_hanoi_value_at_index(generation)
        resident_hanoi_value = surface_hanoi_values[target_site]
        resident_deposition_rank = surface_deposition_ranks[target_site]

        guaranteed_num_reservations = get_num_reservations_provided_impl(
            hanoi_value, surface_size, generation
        )
        for reservation_index in range(guaranteed_num_reservations):
            comparable_reservation_site = get_reservation_pos_impl(
                reservation_index,
                surface_size,
            )
            comparable_value_site = (
                comparable_reservation_site + resident_hanoi_value
            )
            comparable_deposition_rank = surface_deposition_ranks[
                comparable_value_site
            ]

            if (
                comparable_value_site != target_site
                # and hanoi_value == resident_hanoi_value
                and resident_deposition_rank != -1
                and comparable_deposition_rank != -1
                and comparable_deposition_rank < resident_deposition_rank
            ):
                same_hanoi_value_deposition_ranks = [
                    deposition_rank_
                    for (hanoi_value_, deposition_rank_) in zip(
                        surface_hanoi_values, surface_deposition_ranks
                    )
                    if deposition_rank_ != -1
                    and hanoi_value_ == resident_hanoi_value
                    # exclude deposition rank -1 (phony)
                ]
                same_hanoi_value_sites = [
                    site_
                    for site_, hanoi_value_ in enumerate(surface_hanoi_values)
                    if hanoi_value_ == resident_hanoi_value
                ]
                active_same_hanoi_value_sites = [
                    get_reservation_pos_impl(
                        reservation_index,
                        surface_size,
                    )
                    + resident_hanoi_value
                    for reservation_index in range(guaranteed_num_reservations)
                ]
                return {
                    "hanoi value": hanoi_value,
                    "resident hanoi value": resident_hanoi_value,
                    "resident deposition rank": resident_deposition_rank,
                    "comparable deposition rank": comparable_deposition_rank,
                    "comparable reservation site": comparable_reservation_site,
                    "comparable value site": comparable_value_site,
                    "generation": generation,
                    "guaranteed num reservations": (
                        guaranteed_num_reservations
                    ),
                    "reservation index": reservation_index,
                    "same hanoi value deposition ranks": same_hanoi_value_deposition_ranks,
                    "same hanoi value sites": same_hanoi_value_sites,
                    "active same hanoi value sites": (
                        active_same_hanoi_value_sites
                    ),
                    "target site": target_site,
                }

        surface_hanoi_values[target_site] = hanoi_value
        surface_deposition_ranks[target_site] = generation

    return None
