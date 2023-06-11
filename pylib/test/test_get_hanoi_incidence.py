from pylib import get_hanoi_incidence, get_hanoi_val

def test_get_hanoi_incidence():
    hanoi_values = [*map(get_hanoi_val, range(100))]
    for n, hanoi_value in enumerate(hanoi_values):
        assert hanoi_values[:n].count(hanoi_value) == get_hanoi_incidence(n)
