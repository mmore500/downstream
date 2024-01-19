import numpy as np

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_global_epoch,
)
from pylib.hanoi import get_hanoi_value_index_offset


def _expected8(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(3):
        return 0
    elif rank < get_hanoi_value_index_offset(4):
        return 1
    else:
        return 2


def test_get_global_epoch8():
    surface_size = 8
    for rank in range(2**8):
        assert get_global_epoch(rank, surface_size) == _expected8(rank)


def _expected16(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(4):
        return 0
    elif rank < get_hanoi_value_index_offset(5):
        return 1
    elif rank < get_hanoi_value_index_offset(8):
        return 2
    else:
        return 3


def test_get_global_epoch16():
    surface_size = 16
    for rank in range(2**16):
        assert get_global_epoch(rank, surface_size) == _expected16(rank)


def _expected32(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(5):
        return 0
    elif rank < get_hanoi_value_index_offset(6):
        return 1
    elif rank < get_hanoi_value_index_offset(9):
        return 2
    elif rank < get_hanoi_value_index_offset(16):
        return 3
    else:
        return 4


def test_get_global_epoch32():
    surface_size = 32
    for rank in range(2**16):
        assert get_global_epoch(rank, surface_size) == _expected32(rank)

    for rank in np.random.randint(0, 2**32, size=10000):
        rank = int(rank)
        assert get_global_epoch(rank, surface_size) == _expected32(rank)


def _expected64(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(6):
        return 0
    elif rank < get_hanoi_value_index_offset(7):
        return 1
    elif rank < get_hanoi_value_index_offset(10):
        return 2
    elif rank < get_hanoi_value_index_offset(17):
        return 3
    elif rank < get_hanoi_value_index_offset(32):
        return 4
    else:
        return 5


def test_get_global_epoch64():
    surface_size = 64
    for rank in range(2**16):
        assert get_global_epoch(rank, surface_size) == _expected64(rank)

    for rank in np.random.randint(0, 2**63, size=10000):  # signed precision
        rank = int(rank)
        assert get_global_epoch(rank, surface_size) == _expected64(rank)
