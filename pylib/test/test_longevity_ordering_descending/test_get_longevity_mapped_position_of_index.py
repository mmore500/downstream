import pytest

import pylib.longevity_ordering_descending as lod


def test_get_longevity_mapped_position_of_index1():
    assert [
        lod.get_longevity_mapped_position_of_index(
            index,
            1,
        )
        for index in range(1)
    ] == [0]

    target = [None] * 1
    for index in range(1):
        mapped_position = lod.get_longevity_mapped_position_of_index(
            index,
            1,
        )
        target[mapped_position] = index

    assert target == [0]


def test_get_longevity_mapped_position_of_index2():
    assert [
        lod.get_longevity_mapped_position_of_index(
            index,
            2,
        )
        for index in range(2)
    ] == [0, 1]

    target = [None] * 2
    for index in range(2):
        mapped_position = lod.get_longevity_mapped_position_of_index(
            index,
            2,
        )
        target[mapped_position] = index

    assert target == [0, 1]


def test_get_longevity_mapped_position_of_index4():
    assert [
        lod.get_longevity_mapped_position_of_index(
            index,
            4,
        )
        for index in range(4)
    ] == ([0, 2, 3, 1])

    target = [None] * 4
    for index in range(4):
        mapped_position = lod.get_longevity_mapped_position_of_index(
            index,
            4,
        )
        target[mapped_position] = index

    assert target == [0, 3, 1, 2]


def test_get_longevity_mapped_position_of_index8():
    assert [
        lod.get_longevity_mapped_position_of_index(
            index,
            8,
        )
        for index in range(8)
    ] == [0, 4, 6, 2, 3, 7, 5, 1]

    target = [None] * 8
    for index in range(8):
        mapped_position = lod.get_longevity_mapped_position_of_index(
            index,
            8,
        )
        target[mapped_position] = index

    assert target == [0, 7, 3, 4, 1, 6, 2, 5]


def test_get_longevity_mapped_position_of_index16():
    assert [
        lod.get_longevity_mapped_position_of_index(
            index,
            16,
        )
        for index in range(16)
    ] == ([0, 8, 12, 4, 6, 14, 10, 2, 3, 11, 15, 7, 5, 13, 9, 1])

    target = [None] * 16
    for index in range(16):
        mapped_position = lod.get_longevity_mapped_position_of_index(
            index,
            16,
        )
        target[mapped_position] = index

    assert target == ([0, 15, 7, 8, 3, 12, 4, 11, 1, 14, 6, 9, 2, 13, 5, 10])
