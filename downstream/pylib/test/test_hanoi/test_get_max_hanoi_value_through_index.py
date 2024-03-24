from pylib.hanoi import (
    get_hanoi_value_at_index,
    get_max_hanoi_value_through_index,
)


def test_get_max_hanoi_value_through_index():
    hanoi_values = [*map(get_hanoi_value_at_index, range(1000))]
    for n in range(len(hanoi_values)):
        assert max(hanoi_values[: n + 1]) == get_max_hanoi_value_through_index(
            n
        ), n
