import pylib


def test_get_a037870_value_at_index():
    assert [*map(pylib.oeis.get_a037870_value_at_index, range(1, 91),)] == [
        # https://oeis.org/A037870/list
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        2,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        2,
        1,
        1,
        1,
        2,
        2,
        2,
        1,
        2,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        2,
        1,
        1,
        1,
        2,
        2,
        2,
        1,
        2,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        1,
        3,
        2,
        2,
        1,
        2,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        2,
        1,
        1,
        1,
        2,
        2,
        2,
        1,
        2,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        1,
        3,
        2,
        2,
    ]
