import itertools as it

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    get_reservation_position_physical,
)


def test_get_reservation_position_physical4():
    assert [get_reservation_position_physical(r, 4) for r in range(2)] == [
        0,  # 0, over 0
        2,  # 1, over 0
    ]


def test_get_reservation_position_physical8():
    assert [get_reservation_position_physical(r, 8) for r in range(4)] == [
        0,  # 0, over 0
        3,  # 1, over 1
        4,  # 2, over 0
        6,  # 3, over 0
    ]


def test_get_reservation_position_physical16():
    assert [get_reservation_position_physical(r, 16) for r in range(8)] == [
        0,  # 0, over 0
        4,  # 1, over 2
        5,  # 2, over 1
        7,  # 3, over 1
        8,  # 4, over 0
        11,  # 5, over 1
        12,  # 6, over 0
        14,  # 7, over 0
    ]


def test_get_reservation_position_physical32():
    assert [get_reservation_position_physical(r, 32) for r in range(16)] == [
        0,  # 0, over 0
        5,  # 1, over 3
        6,  # 2, over 2
        8,  # 3, over 2
        9,  # 4, over 1
        12,  # 5, over 2
        13,  # 6, over 1
        15,  # 7, over 1
        16,  # 8, over 0
        20,  # 9, over 2
        21,  # 10, over 1
        23,  # 11, over 1
        24,  # 12, over 0
        27,  # 13, over 1
        28,  # 14, over 0
        30,  # 15, over 0
    ]


def test_get_reservation_position_physical64():
    assert all(
        a < b
        for a, b in it.pairwise(
            get_reservation_position_physical(r, 64) for r in range(32)
        )
    )
    assert get_reservation_position_physical(0, 64) == 0
    assert get_reservation_position_physical(16, 64) == 32
    assert get_reservation_position_physical(31, 64) == 62
