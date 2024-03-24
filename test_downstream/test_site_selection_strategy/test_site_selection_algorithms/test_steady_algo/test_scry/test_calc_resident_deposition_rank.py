import itertools as it
import typing

import pytest

from downstream.downstream import steady_algo as algo


@pytest.mark.parametrize(
    "surface_size",
    [2**x for x in range(1, 10)]
    + [pytest.param(2**x, marks=pytest.mark.heavy) for x in range(6, 11)],
)
@pytest.mark.parametrize(
    "num_generations_bidder",
    [
        lambda surface_size: 2**15 // surface_size,
        pytest.param(
            lambda surface_size: 2**18 // max(1, surface_size >> 9),
            marks=pytest.mark.heavy,
        ),
    ],
)
def test_calc_resident_deposition_rank_integration(
    surface_size: int,
    num_generations_bidder: typing.Callable,
):
    num_generations = num_generations_bidder(surface_size)
    surface_deposition_ranks = [0] * surface_size
    for rank in range(num_generations):
        for site, actual_deposition_rank in enumerate(
            surface_deposition_ranks
        ):
            calculated_deposition_rank = algo.calc_resident_deposition_rank(
                site,
                surface_size,
                rank,
            )
            assert calculated_deposition_rank == actual_deposition_rank, {
                "actual deposition rank": actual_deposition_rank,
                "calculated deposition rank": calculated_deposition_rank,
                "num depositions": rank,
                "rank": rank,
                "site": site,
            }

        assert all(
            it.starmap(
                int.__eq__,
                zip(
                    [*algo.iter_resident_deposition_ranks(surface_size, rank)],
                    surface_deposition_ranks,
                    strict=True,
                ),
            )
        )

        # update surface
        target_site = algo.pick_deposition_site(rank, surface_size)
        surface_deposition_ranks[target_site] = rank
