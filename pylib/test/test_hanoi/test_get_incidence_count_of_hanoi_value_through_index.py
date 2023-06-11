import itertools as it

from pylib.hanoi import (
    get_incidence_count_of_hanoi_value_through_index,
    get_hanoi_value_at_index,
)


def test_get_incidence_count_of_hanoi_value_through_index():
    hanoi_values = [*map(get_hanoi_value_at_index, range(1000))]
    for n, hanoi_value in it.product(
        range(len(hanoi_values)),
        range(20),
    ):
        assert hanoi_values[: n + 1].count(
            hanoi_value
        ) == get_incidence_count_of_hanoi_value_through_index(hanoi_value, n), (
            n,
            hanoi_value,
        )
