import numpy as np
import pytest

from pylib import hanoi


@pytest.mark.parametrize("incidence", [*range(4), 7, 10, 101])
@pytest.mark.parametrize(
    "index",
    [
        *range(100),
        *map(int, np.linspace(0, 2**62, 100, dtype=int)),
        *map(int, np.geomspace(1, 2**62, 100, dtype=int)),
        *map(int, np.random.RandomState(seed=1).randint(0, 2**62, 100)),
    ],
)
def test_get_min_hanoi_value_with_incidence_at_least(
    incidence: int, index: int
):
    assert hanoi.get_min_hanoi_value_with_incidence_at_least(
        incidence, index
    ) == next(
        (
            hv
            for hv in reversed(
                range(hanoi.get_max_hanoi_value_through_index(index) + 1)
            )
            if hanoi.get_index_of_hanoi_value_nth_incidence(hv, incidence)
            <= index
        ),
        None,
    )
