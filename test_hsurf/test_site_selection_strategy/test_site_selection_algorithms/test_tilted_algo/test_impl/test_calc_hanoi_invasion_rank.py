from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    calc_hanoi_invasion_rank,
)


def test_calc_hanoi_invasion_rank8():
    assert calc_hanoi_invasion_rank(0, epoch=1, surface_size=8) == 2**3 - 1
    assert calc_hanoi_invasion_rank(0, epoch=2, surface_size=8) == 2**4 - 1
    assert calc_hanoi_invasion_rank(1, epoch=2, surface_size=8) == 2**5 - 1
    assert calc_hanoi_invasion_rank(2, epoch=2, surface_size=8) == 2**6 - 1
    assert calc_hanoi_invasion_rank(3, epoch=2, surface_size=8) == 2**7 - 1


def test_calc_hanoi_invasion_rank16():
    assert calc_hanoi_invasion_rank(0, epoch=1, surface_size=16) == 2**4 - 1
    assert calc_hanoi_invasion_rank(0, epoch=2, surface_size=16) == 2**5 - 1
    assert calc_hanoi_invasion_rank(1, epoch=2, surface_size=16) == 2**6 - 1
    assert calc_hanoi_invasion_rank(2, epoch=2, surface_size=16) == 2**7 - 1
    assert calc_hanoi_invasion_rank(0, epoch=3, surface_size=16) == 2**8 - 1
    assert calc_hanoi_invasion_rank(1, epoch=3, surface_size=16) == 2**9 - 1
    assert calc_hanoi_invasion_rank(2, epoch=3, surface_size=16) == 2**10 - 1
    assert calc_hanoi_invasion_rank(3, epoch=3, surface_size=16) == 2**11 - 1
    assert calc_hanoi_invasion_rank(4, epoch=3, surface_size=16) == 2**12 - 1
    assert calc_hanoi_invasion_rank(5, epoch=3, surface_size=16) == 2**13 - 1
    assert calc_hanoi_invasion_rank(6, epoch=3, surface_size=16) == 2**14 - 1
    assert calc_hanoi_invasion_rank(7, epoch=3, surface_size=16) == 2**15 - 1
