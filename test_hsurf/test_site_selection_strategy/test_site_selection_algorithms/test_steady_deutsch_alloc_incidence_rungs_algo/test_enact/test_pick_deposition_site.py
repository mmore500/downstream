import numpy as np
import pytest

from hsurf.hsurf import steady_deutsch_alloc_incidence_rungs_algo as algo
from hsurf.pylib.hanoi import (
    get_hanoi_value_at_index,
    get_incidence_count_of_hanoi_value_through_index,
)


@pytest.mark.parametrize("surface_size", [8, 16, 32, 64, 128])
@pytest.mark.parametrize(
    "rank",
    [
        *range(300),
        *map(int, np.linspace(0, 2**62, 10**2, dtype=int)),
        *map(int, np.geomspace(1, 2**62, 10**2, dtype=int)),
        *map(int, np.random.RandomState(seed=1).randint(0, 2**62, 10**2)),
    ],
)
def test_pick_deposition_site_smoke(surface_size: int, rank: int) -> int:
    # just a smoke test
    deposit_site = algo.pick_deposition_site(rank, surface_size)
    assert isinstance(deposit_site, int)
    assert 0 <= deposit_site < surface_size


@pytest.mark.parametrize("surface_size", [2**exp for exp in range(2, 12)])
@pytest.mark.parametrize(
    "num_generations",
    [2**12, pytest.param(2**18, marks=pytest.mark.heavy)],
)
def test_pick_deposition_site_hanoi_value_overwrite_order(
    surface_size: int,
    num_generations: int,
):
    num_available_bins = surface_size // 2
    surface_hanoi_values = [-1] * surface_size
    for rank in range(num_generations):
        target_site = algo.pick_deposition_site(rank, surface_size)
        deposited_hanoi_value = get_hanoi_value_at_index(rank)
        deposited_hanoi_incidence = (
            get_incidence_count_of_hanoi_value_through_index(
                deposited_hanoi_value, rank
            )
        )
        resident_hanoi_value = surface_hanoi_values[target_site]
        surface_hanoi_values[target_site] = deposited_hanoi_value
        if resident_hanoi_value == -1:
            continue
        resident_hanoi_incidence = (
            get_incidence_count_of_hanoi_value_through_index(
                resident_hanoi_value, rank
            )
        )
        assert resident_hanoi_incidence >= num_available_bins
        if deposited_hanoi_incidence <= num_available_bins:
            assert deposited_hanoi_value > resident_hanoi_value
