import pylib


def test_get_longevity_position_within_level1():
    assert [
        pylib.longevity_ordering_naive.get_longevity_position_within_level(
            index,
            1,
        )
        for index in range(1)
    ] == [0]


def test_get_longevity_position_within_level2():
    assert [
        pylib.longevity_ordering_naive.get_longevity_position_within_level(
            index,
            2,
        )
        for index in range(2)
    ] == [0, 0]


def test_get_longevity_position_within_level4():
    assert [
        pylib.longevity_ordering_naive.get_longevity_position_within_level(
            index,
            4,
        )
        for index in range(4)
    ] == [0, 0, 0, 1]


def test_get_longevity_position_within_level8():
    assert [
        pylib.longevity_ordering_naive.get_longevity_position_within_level(
            index,
            8,
        )
        for index in range(8)
    ] == [0, 0, 0, 1, 0, 2, 1, 3]


def test_get_longevity_position_within_level16():
    assert [
        pylib.longevity_ordering_naive.get_longevity_position_within_level(
            index,
            16,
        )
        for index in range(16)
    ] == [0, 0, 0, 1, 0, 2, 1, 3, 0, 4, 2, 5, 1, 6, 3, 7]
