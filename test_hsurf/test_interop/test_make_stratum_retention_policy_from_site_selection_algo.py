import types

import pytest

from hsurf import hsurf


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_GenDropRanks(interop_algo: types.ModuleType, surface_size: int):
    policy = interop_algo.Policy(surface_size)

    for rank in range(surface_size):
        assert [*policy.GenDropRanks(rank)] == []

    for rank in range(surface_size, 100):
        site = interop_algo._site_selection_algo.pick_deposition_site(
            rank, surface_size
        )
        assert [*policy.GenDropRanks(rank)] == [
            interop_algo._site_selection_algo.calc_resident_deposition_rank(
                site, surface_size, rank - 1
            )
        ]


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcNumStrataRetainedExact(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)

    for rank in range(200):
        assert policy.CalcNumStrataRetainedExact(rank) == min(
            rank, surface_size
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcRankAtColumnIndex(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)

    assert policy.CalcNumStrataRetainedExact(0) == 0
    for rank in range(1, 100):
        column_ranks = [
            policy.CalcRankAtColumnIndex(index, rank)
            for index in range(policy.CalcNumStrataRetainedExact(rank))
        ]
        assert column_ranks == sorted(
            set(  # have to deduplicate rank 0 entries
                interop_algo._site_selection_algo.iter_resident_deposition_ranks(
                    surface_size, rank
                ),
            ),
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcNumStrataRetainedUpperBound(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)

    for rank in range(200):
        assert policy.CalcNumStrataRetainedExact(
            rank
        ) <= policy.CalcNumStrataRetainedUpperBound(rank)
