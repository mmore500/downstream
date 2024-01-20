from hsurf.pylib.hanoi import get_hanoi_value_index_offset
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_epoch_rank,
)


def test_get_epoch_rank8():
    assert get_epoch_rank(0, 8) == 0
    assert get_epoch_rank(1, 8) == get_hanoi_value_index_offset(3)
    assert get_epoch_rank(2, 8) == get_hanoi_value_index_offset(4)


def test_get_epoch_rank16():
    assert get_epoch_rank(0, 16) == 0
    assert get_epoch_rank(1, 16) == get_hanoi_value_index_offset(4)
    assert get_epoch_rank(2, 16) == get_hanoi_value_index_offset(5)
    assert get_epoch_rank(3, 16) == get_hanoi_value_index_offset(8)


def test_get_epoch_rank32():
    assert get_epoch_rank(0, 32) == 0
    assert get_epoch_rank(1, 32) == get_hanoi_value_index_offset(5)
    assert get_epoch_rank(2, 32) == get_hanoi_value_index_offset(6)
    assert get_epoch_rank(3, 32) == get_hanoi_value_index_offset(9)
    assert get_epoch_rank(4, 32) == get_hanoi_value_index_offset(16)


def test_get_epoch_rank64():
    assert get_epoch_rank(0, 64) == 0
    assert get_epoch_rank(1, 64) == get_hanoi_value_index_offset(6)
    assert get_epoch_rank(2, 64) == get_hanoi_value_index_offset(7)
    assert get_epoch_rank(3, 64) == get_hanoi_value_index_offset(10)
    assert get_epoch_rank(4, 64) == get_hanoi_value_index_offset(17)
    assert get_epoch_rank(5, 64) == get_hanoi_value_index_offset(32)
