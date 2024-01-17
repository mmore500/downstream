from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    get_reservation_position_logical,
)


def test_get_reservation_position_logical4():
    assert [get_reservation_position_logical(r, 4) for r in range(2)] == [
        0,  # 0, over 0
        3,  # 1, over 0
    ]


def test_get_reservation_position_logical8():
    assert [get_reservation_position_logical(r, 8) for r in range(4)] == [
        0,  # 0, over 0
        5,  # 2, over 0
        4,  # 1, over 1
        7,  # 3, over 0
    ]


def test_get_reservation_position_logical16():
    assert [get_reservation_position_logical(r, 16) for r in range(8)] == [
        0,  # 0, over 0
        9,  # 4, over 0
        6,  # 2, over 1
        13,  # 6, over 0
        5,  # 1, over 2
        8,  # 3, over 1
        12,  # 5, over 1
        15,  # 7, over 0
    ]


def test_get_reservation_position_logical32():
    assert [get_reservation_position_logical(r, 32) for r in range(16)] == [
        0,  # 0, over 0
        17,  # 8, over 0
        10,  # 4, over 1
        25,  # 12, over 0
        7,  # 2, over 2
        14,  # 6, over 1
        22,  # 10, over 1
        29,  # 14, over 0
        6,  # 1, over 3
        9,  # 3, over 2
        13,  # 5, over 2
        16,  # 7, over 1
        21,  # 9, over 2
        24,  # 11, over 1
        28,  # 13, over 1
        31,  # 15, over 0
    ]


def test_get_reservation_position_logical64():
    assert all(
        0 <= get_reservation_position_logical(r, 64) < 64 for r in range(32)
    )
    assert (
        len(set(get_reservation_position_logical(r, 64) for r in range(32)))
        == 32
    )
    assert get_reservation_position_logical(0, 64) == 0
    assert get_reservation_position_logical(1, 64) == 33
    assert get_reservation_position_logical(31, 64) == 63
