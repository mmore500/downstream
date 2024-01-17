from pylib import oeis


def test_get_a005187_index_of_value():
    for i in range(2000):
        n = oeis.get_a005187_index_of_value(i)
        lb = oeis.get_a005187_value_at_index(n)
        ub = oeis.get_a005187_value_at_index(n + 1)
        assert lb <= i < ub
