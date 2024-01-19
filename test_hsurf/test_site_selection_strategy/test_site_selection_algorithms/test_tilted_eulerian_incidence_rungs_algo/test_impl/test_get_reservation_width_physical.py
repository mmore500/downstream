from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    get_reservation_width_physical,
)


def test_get_reservation_width_physical4():
    assert [get_reservation_width_physical(r, 4) for r in range(2)] == [
        3,  # 1, over 0
        1,
    ]


def test_get_reservation_width_physical8():
    assert [get_reservation_width_physical(r, 8) for r in range(4)] == [
        4,  # 1, over 1
        1,  # 2, over 0
        2,  # 3, over 0
        1,
    ]


def test_get_reservation_width_physical16():
    assert [get_reservation_width_physical(r, 16) for r in range(8)] == [
        5,  # 1, over 2
        1,  # 2, over 1
        2,  # 3, over 1
        1,  # 4, over 0
        3,  # 5, over 1
        1,  # 6, over 0
        2,  # 7, over 0
        1,
    ]


def test_get_reservation_width_physical32():
    assert [get_reservation_width_physical(r, 32) for r in range(16)] == [
        6,  # 1, over 3
        1,  # 2, over 2
        2,  # 3, over 2
        1,  # 4, over 1
        3,  # 5, over 2
        1,  # 6, over 1
        2,  # 7, over 1
        1,  # 8, over 0
        4,  # 9, over 2
        1,  # 10, over 1
        2,  # 11, over 1
        1,  # 12, over 0
        3,  # 13, over 1
        1,  # 14, over 0
        2,  # 15, over 0
        1,  # 0, over 0
    ]


def test_get_reservation_width_physical64():
    assert get_reservation_width_physical(0, 64) == 7
    assert get_reservation_width_physical(16, 64) == 5
    assert get_reservation_width_physical(31, 64) == 1
