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
