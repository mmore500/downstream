import pylib


def test_get_longevity_ordered_position_of_index():
    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            level,
            1,
        )
        for level in range(1)
    ] == [0]

    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            level,
            2,
        )
        for level in range(2)
    ] == [0, 1]

    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            level,
            4,
        )
        for level in range(4)
    ] == [0, 2, 1, 3]

    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            level,
            8,
        )
        for level in range(8)
    ] == [0, 4, 2, 6, 1, 3, 5, 7]

    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            level,
            16,
        )
        for level in range(16)
    ] == [0, 8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
