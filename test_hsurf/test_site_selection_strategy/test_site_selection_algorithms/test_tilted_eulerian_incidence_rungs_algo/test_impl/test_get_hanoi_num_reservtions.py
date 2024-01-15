import numpy as np

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    get_global_num_reservations,
    get_hanoi_num_reservations,
)
from pylib import hanoi


def test_get_hanoi_num_reservations8():
    surface_size = 8
    for rank in range(2**8):
        hnr = get_hanoi_num_reservations(rank, surface_size)
        gnr = get_global_num_reservations(rank, surface_size)
        assert hnr in (gnr, gnr * 2)

    for rank in range(7):
        assert hanoi.get_max_hanoi_value_through_index(rank) <= 2
        assert get_hanoi_num_reservations(rank, surface_size) == 4

    for rank in range(7, 15):
        assert hanoi.get_max_hanoi_value_through_index(rank) == 3
        assert get_hanoi_num_reservations(rank, surface_size) == 2

    for rank in range(15, 31):
        assert hanoi.get_max_hanoi_value_through_index(rank) == 4
        if hanoi.get_hanoi_value_at_index(rank) in (1, 2):
            assert get_hanoi_num_reservations(rank, surface_size) == 2
        else:
            assert get_hanoi_num_reservations(rank, surface_size) == 1

    for rank in range(31, 63):
        assert hanoi.get_max_hanoi_value_through_index(rank) == 5
        if hanoi.get_hanoi_value_at_index(rank) == 2:
            assert get_hanoi_num_reservations(rank, surface_size) == 2
        else:
            assert get_hanoi_num_reservations(rank, surface_size) == 1

    for rank in range(63, 127):
        assert hanoi.get_max_hanoi_value_through_index(rank) == 6
        assert get_hanoi_num_reservations(rank, surface_size) == 1


def test_get_hanoi_num_reservations16():
    surface_size = 16
    for rank in range(2**16):
        hnr = get_hanoi_num_reservations(rank, surface_size)
        gnr = get_global_num_reservations(rank, surface_size)
        assert hnr in (gnr, gnr * 2)


def test_get_hanoi_num_reservations32():
    surface_size = 32
    for rank in range(2**16):
        hnr = get_hanoi_num_reservations(rank, surface_size)
        gnr = get_global_num_reservations(rank, surface_size)
        assert hnr in (gnr, gnr * 2)

    for rank in np.random.randint(0, 2**32, size=10000):
        rank = int(rank)
        hnr = get_hanoi_num_reservations(rank, surface_size)
        gnr = get_global_num_reservations(rank, surface_size)
        assert hnr in (gnr, gnr * 2)


def test_get_hanoi_num_reservations64():
    surface_size = 64
    for rank in range(2**16):
        hnr = get_hanoi_num_reservations(rank, surface_size)
        gnr = get_global_num_reservations(rank, surface_size)
        assert hnr in (gnr, gnr * 2)

    for rank in np.random.randint(0, 2**63, size=10000):  # signed precision
        rank = int(rank)
        hnr = get_hanoi_num_reservations(rank, surface_size)
        gnr = get_global_num_reservations(rank, surface_size)
        assert hnr in (gnr, gnr * 2)
