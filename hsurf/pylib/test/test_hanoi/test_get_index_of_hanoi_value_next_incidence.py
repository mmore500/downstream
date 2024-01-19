import pytest

from pylib.hanoi import (
    get_index_of_hanoi_value_next_incidence,
    get_index_of_hanoi_value_nth_incidence,
)


@pytest.mark.parametrize("hanoi_value", range(1, 6))
@pytest.mark.parametrize("i", range(5))
def test_get_index_of_hanoi_value_next_incidence(hanoi_value, i):
    lb = get_index_of_hanoi_value_nth_incidence(hanoi_value, i)
    ub = get_index_of_hanoi_value_nth_incidence(hanoi_value, i + 1)
    for index in range(lb, ub):
        assert (
            get_index_of_hanoi_value_next_incidence(
                hanoi_value,
                index,
            )
            == ub
        )
    for index in range(0, lb):
        assert (
            get_index_of_hanoi_value_next_incidence(
                hanoi_value,
                index,
            )
            <= lb
            < ub
        )
    assert (
        get_index_of_hanoi_value_next_incidence(
            hanoi_value,
            ub,
        )
        > ub
    )
