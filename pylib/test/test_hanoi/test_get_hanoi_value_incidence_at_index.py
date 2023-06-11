from pylib.hanoi import get_hanoi_value_incidence_at_index, get_hanoi_value_at_index


def test_get_hanoi_value_incidence_at_index():
    hanoi_values = [*map(get_hanoi_value_at_index, range(100))]
    for n, hanoi_value in enumerate(hanoi_values):
        assert hanoi_values[:n].count(
            hanoi_value
        ) == get_hanoi_value_incidence_at_index(n)
