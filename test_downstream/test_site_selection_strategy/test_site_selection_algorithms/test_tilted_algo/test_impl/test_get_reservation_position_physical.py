import itertools as it

from downstream.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_reservation_position_physical,
)


def test_get_reservation_position_physical4():
    assert [get_reservation_position_physical(r, 4) for r in range(2)] == [
        0,  # 0, over 0
        3,  # 1, over 0
    ]


def test_get_reservation_position_physical8():
    assert [get_reservation_position_physical(r, 8) for r in range(4)] == [
        0,  # 0, over 0
        4,  # 1, over 1
        5,  # 2, over 0
        7,  # 3, over 0
    ]


def test_get_reservation_position_physical16():
    assert [get_reservation_position_physical(r, 16) for r in range(8)] == [
        0,  # 0, over 0
        5,  # 1, over 2
        6,  # 2, over 1
        8,  # 3, over 1
        9,  # 4, over 0
        12,  # 5, over 1
        13,  # 6, over 0
        15,  # 7, over 0
    ]


def test_get_reservation_position_physical32():
    assert [get_reservation_position_physical(r, 32) for r in range(16)] == [
        0,  # 0, over 0
        6,  # 1, over 3
        7,  # 2, over 2
        9,  # 3, over 2
        10,  # 4, over 1
        13,  # 5, over 2
        14,  # 6, over 1
        16,  # 7, over 1
        17,  # 8, over 0
        21,  # 9, over 2
        22,  # 10, over 1
        24,  # 11, over 1
        25,  # 12, over 0
        28,  # 13, over 1
        29,  # 14, over 0
        31,  # 15, over 0
    ]


def test_get_reservation_position_physical64():
    assert all(
        a < b
        for a, b in it.pairwise(
            get_reservation_position_physical(r, 64) for r in range(32)
        )
    )
    assert get_reservation_position_physical(0, 64) == 0
    assert get_reservation_position_physical(16, 64) == 33
    assert get_reservation_position_physical(31, 64) == 63
