import pylib


def test_get_a000295_value_at_index():
    assert [*map(pylib.oeis.get_a000295_index_of_value, range(15))] == [
        # https://oeis.org/A000295/list
        # note: skips zeroth element
        0,  # 0
        1,  # 1
        1,  # 2
        1,  # 3
        2,  # 4
        2,  # 5
        2,  # 6
        2,  # 7
        2,  # 8
        2,  # 9
        2,  # 10
        3,  # 11
        3,  # 12
        3,  # 13
        3,  # 14
    ]


for i in range(400):
    n = pylib.oeis.get_a000295_index_of_value(i)
    lb, ub = pylib.oeis.get_a000295_value_at_index(
        n
    ), pylib.oeis.get_a000295_value_at_index(n + 1)
    assert (
        pylib.oeis.get_a000295_value_at_index(n)
        <= i
        < pylib.oeis.get_a000295_value_at_index(n + 1)
    )
