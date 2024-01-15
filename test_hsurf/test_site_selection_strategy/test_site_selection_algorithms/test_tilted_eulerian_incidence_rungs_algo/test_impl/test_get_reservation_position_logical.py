import itertools as it

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    get_reservation_position_logical,
)


def test_get_reservation_position_logical4():
    assert [get_reservation_position_logical(r, 4) for r in range(2)] == [
        0,  # 0, over 0
        2,  # 1, over 0
    ]


def test_get_reservation_position_logical8():
    assert [get_reservation_position_logical(r, 8) for r in range(4)] == [
        0,  # 0, over 0
        4,  # 2, over 0
        3,  # 1, over 1
        6,  # 3, over 0
    ]


def test_get_reservation_position_logical16():
    assert [get_reservation_position_logical(r, 16) for r in range(8)] == [
        0,  # 0, over 0
        8,  # 4, over 0
        5,  # 2, over 1
        12,  # 6, over 0
        4,  # 1, over 2
        7,  # 3, over 1
        11,  # 5, over 1
        14,  # 7, over 0
    ]


def test_get_reservation_position_logical32():
    assert [get_reservation_position_logical(r, 32) for r in range(16)] == [
        0,  # 0, over 0
        16,  # 8, over 0
        9,  # 4, over 1
        24,  # 12, over 0
        6,  # 2, over 2
        13,  # 6, over 1
        21,  # 10, over 1
        28,  # 14, over 0
        5,  # 1, over 3
        8,  # 3, over 2
        12,  # 5, over 2
        15,  # 7, over 1
        20,  # 9, over 2
        23,  # 11, over 1
        27,  # 13, over 1
        30,  # 15, over 0
    ]


def test_get_reservation_position_logical64():
    assert all(
        0 <= get_reservation_position_logical(r, 64) < 63 for r in range(32)
    )
    assert (
        len(set(get_reservation_position_logical(r, 64) for r in range(32)))
        == 32
    )
    assert get_reservation_position_logical(0, 64) == 0
    assert get_reservation_position_logical(1, 64) == 32
    assert get_reservation_position_logical(31, 64) == 62
