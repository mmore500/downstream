import types

import pytest

from downstream import downstream


@pytest.mark.parametrize(
    "site_selection_algo",
    [
        downstream.hybrid_algo,
        downstream.steady_algo,
        downstream.tilted_algo,
        downstream.tilted_sticky_algo,
    ],
)
def test_sort_differentiae_by_deposition_rank(
    site_selection_algo: types.ModuleType,
):
    surface_size = 16
    surface = [0] * surface_size

    for rank in range(surface_size * 2):
        site = site_selection_algo.pick_deposition_site(rank, surface_size)
        surface[site] = rank % 7

    sorted_differentiae = downstream.sort_differentiae_by_deposition_rank(
        surface,
        num_strata_deposited=rank + 1,
        site_selection_algo=site_selection_algo,
    )

    assert sorted_differentiae == [
        rank % 7
        for rank in sorted(
            site_selection_algo.iter_resident_deposition_ranks(
                surface_size, rank + 1
            ),
        )
    ]


@pytest.mark.parametrize(
    "site_selection_algo",
    [
        downstream.hybrid_algo,
        downstream.steady_algo,
        downstream.tilted_algo,
        downstream.tilted_sticky_algo,
    ],
)
def test_sort_differentiae_by_deposition_rank_founders(
    site_selection_algo: types.ModuleType,
):
    surface_size = 16
    surface = [0] * surface_size

    short_by = 3
    for rank in range(surface_size - short_by):
        site = site_selection_algo.pick_deposition_site(rank, surface_size)
        surface[site] = rank % 7

    sorted_differentiae = downstream.sort_differentiae_by_deposition_rank(
        surface,
        num_strata_deposited=rank + 1,
        site_selection_algo=site_selection_algo,
    )
    assert len(sorted_differentiae) == surface_size - short_by

    assert (
        sorted_differentiae
        == [
            rank % 7
            for rank in sorted(
                site_selection_algo.iter_resident_deposition_ranks(
                    surface_size, rank + 1
                ),
            )
        ][short_by:]
    )


@pytest.mark.parametrize(
    "site_selection_algo",
    [
        downstream.hybrid_algo,
        downstream.steady_algo,
        downstream.tilted_algo,
        downstream.tilted_sticky_algo,
    ],
)
def test_sort_differentiae_by_deposition_rank_firstfounder(
    site_selection_algo: types.ModuleType,
):
    surface_size = 16
    surface = [0] * surface_size
    surface[0] = 101

    short_by = 3
    for rank in range(surface_size - short_by):
        site = site_selection_algo.pick_deposition_site(rank, surface_size)
        surface[site] = (rank % 7) if (site or rank) else 101

    assert surface[0] == 101
    sorted_differentiae = downstream.sort_differentiae_by_deposition_rank(
        surface,
        num_strata_deposited=rank + 1,
        site_selection_algo=site_selection_algo,
    )
    assert len(sorted_differentiae) == surface_size - short_by
    assert sorted_differentiae[0] == 101
