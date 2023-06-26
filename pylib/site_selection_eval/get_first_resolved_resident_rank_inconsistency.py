import typing


def get_first_resolved_resident_rank_inconsistency(
    get_deposition_site_at_rank_impl: typing.Callable,
    get_deposition_rank_at_site_impl: typing.Callable,
    surface_size: int,
    num_generations: int,
    progress_wrap: typing.Callable = lambda x: x,
) -> typing.Optional[typing.Dict]:

    surface_deposition_ranks = [0] * surface_size

    for generation in progress_wrap(range(num_generations)):
        target_site = get_deposition_site_at_rank_impl(
            generation, surface_size
        )
        surface_deposition_ranks[target_site] = generation

        for site in range(surface_size):
            actual_timestamp = surface_deposition_ranks[target_site]
            expected_timestamp = get_deposition_rank_at_site_impl(
                site,
                surface_size,
                generation + 1,
            )
            if actual_timestamp != expected_timestamp:
                return {
                    "actual deposition rank": actual_deposition_rank,
                    "expected deposition rank": expected_deposition_rank,
                    "generation": generation + 1,
                    "site": site,
                }

    return None
