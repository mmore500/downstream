from pylib import oeis


def test_get_a059893_index_of_value():
    for n in range(2000):
        assert (
            oeis.get_a059893_value_at_index(oeis.get_a059893_index_of_value(n))
            == n
        )
        assert (
            oeis.get_a059893_index_of_value(oeis.get_a059893_value_at_index(n))
            == n
        )
