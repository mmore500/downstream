import pytest

from pylib import longevity_ordering_alternating as loa


def test_reversed_position_within_level_0():
    assert loa.get_longevity_reversed_position_within_level(0, 0) == 0

def test_reversed_position_within_level_1():
    assert loa.get_longevity_reversed_position_within_level(0, 1) == 0

def test_reversed_position_within_level_2():
    assert loa.get_longevity_reversed_position_within_level(0, 2) == 1
    assert loa.get_longevity_reversed_position_within_level(1, 2) == 0

def test_reversed_position_within_level_3():
    assert loa.get_longevity_reversed_position_within_level(0, 3) == 3
    assert loa.get_longevity_reversed_position_within_level(1, 3) == 2
    assert loa.get_longevity_reversed_position_within_level(2, 3) == 1
    assert loa.get_longevity_reversed_position_within_level(3, 3) == 0
