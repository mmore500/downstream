import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._scry._impl import (
    calc_reservation_reference_incidence,
)

from ._impl import make_reference_incidence_df


@pytest.mark.parametrize(
    "surface_size",
    [
        16,
        pytest.param(32, marks=pytest.mark.heavy),
        pytest.param(64, marks=pytest.mark.heavy),
    ],
)
@pytest.mark.parametrize(
    "max_generations",
    [
        2**9,
        pytest.param(2**12, marks=pytest.mark.heavy),
    ],
)
def test_calc_reservation_reference_incidence(
    surface_size: int, max_generations: int
):
    reference_incidence_df = make_reference_incidence_df(
        surface_size, max_generations
    )
    for index, row in reference_incidence_df.iterrows():
        actual = calc_reservation_reference_incidence(
            int(row["hanoi value"]),
            int(row["reservation index"]),
            surface_size,
            int(row["rank"]),
        )
        expected = row["deposition reference incidence"]
        assert actual == expected, {
            "actual": actual,
            "expected": expected,
            "row": row,
        }
