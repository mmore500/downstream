from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    calc_invading_hanoi_value,
)


def test_calc_invading_hanoi_value8():
    assert calc_invading_hanoi_value(0, epoch=1, surface_size=8) == 3
    assert calc_invading_hanoi_value(0, epoch=2, surface_size=8) == 4
    assert calc_invading_hanoi_value(1, epoch=2, surface_size=8) == 5
    assert calc_invading_hanoi_value(2, epoch=2, surface_size=8) == 6


def test_calc_invading_hanoi_value16():
    assert calc_invading_hanoi_value(0, epoch=1, surface_size=16) == 4
    assert calc_invading_hanoi_value(0, epoch=2, surface_size=16) == 5
    assert calc_invading_hanoi_value(1, epoch=2, surface_size=16) == 6
    assert calc_invading_hanoi_value(2, epoch=2, surface_size=16) == 7
    assert calc_invading_hanoi_value(0, epoch=3, surface_size=16) == 8
    assert calc_invading_hanoi_value(1, epoch=3, surface_size=16) == 9
    assert calc_invading_hanoi_value(2, epoch=3, surface_size=16) == 10
    assert calc_invading_hanoi_value(3, epoch=3, surface_size=16) == 11
    assert calc_invading_hanoi_value(4, epoch=3, surface_size=16) == 12
    assert calc_invading_hanoi_value(5, epoch=3, surface_size=16) == 13
    assert calc_invading_hanoi_value(6, epoch=3, surface_size=16) == 14
    assert calc_invading_hanoi_value(7, epoch=3, surface_size=16) == 15
