import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo import (
    pick_deposition_site as reference_pick_deposition_site,
)
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_sticky_algo import (
    pick_deposition_site as pick_deposition_site,
)


@pytest.mark.parametrize(
    "surface_size, num_generations",
    [
        (8, 254),
        (16, 2**12),
        (32, 2**12),
        (64, 2**12),
    ],
)
def test_vs_reference(surface_size: int, num_generations: int):
    for rank in range(num_generations):
        expected = reference_pick_deposition_site(rank, surface_size)
        res = pick_deposition_site(rank, surface_size)
        assert (expected == res) == bool(expected)
