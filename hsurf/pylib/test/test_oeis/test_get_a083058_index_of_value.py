import pytest

from pylib import oeis


@pytest.mark.parametrize("value", range(1, 1000))
def test_get_a083058_index_of_value(value: int):
    index = oeis.get_a083058_index_of_value(value)
    assert value == oeis.get_a083058_value_at_index(index)
    assert value != oeis.get_a083058_value_at_index(index - 1)
