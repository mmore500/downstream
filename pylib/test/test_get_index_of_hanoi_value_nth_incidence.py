import pytest

from pylib import (
    get_hanoi_value,
    get_index_of_hanoi_value_nth_incidence,
)

@pytest.mark.parametrize("hanoi_value", range(1, 6))
@pytest.mark.parametrize("i", range(5))
def test_get_index_of_hanoi_value_incidence(hanoi_value, i):
    index = get_index_of_hanoi_value_nth_incidence(hanoi_value, i)
    assert get_hanoi_value(index) == hanoi_value
    hanoi_values = [*map(get_hanoi_value, range(index))]
    assert hanoi_values.count(hanoi_value) == i
