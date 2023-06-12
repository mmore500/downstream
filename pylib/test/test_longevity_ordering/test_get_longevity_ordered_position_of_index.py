import pylib


def test_get_longevity_ordered_position_of_index1():
    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            index,
            1,
        )
        for index in range(1)
    ] == [0]

    target = [None] * 1
    for index in range(1):
        mapped_position = (
            pylib.longevity_ordering.get_longevity_ordered_position_of_index(
                index,
                1,
            )
        )
        target[mapped_position] = index

    assert target == [0]


def test_get_longevity_ordered_position_of_index2():
    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            index,
            2,
        )
        for index in range(2)
    ] == [0, 1]

    target = [None] * 2
    for index in range(2):
        mapped_position = (
            pylib.longevity_ordering.get_longevity_ordered_position_of_index(
                index,
                2,
            )
        )
        target[mapped_position] = index

    assert target == [0, 1]


def test_get_longevity_ordered_position_of_index4():
    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            index,
            4,
        )
        for index in range(4)
    ] == [0, 2, 1, 3]

    target = [None] * 4
    for index in range(4):
        mapped_position = (
            pylib.longevity_ordering.get_longevity_ordered_position_of_index(
                index,
                4,
            )
        )
        target[mapped_position] = index

    assert target == [0, 2, 1, 3]


def test_get_longevity_ordered_position_of_index8():
    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            index,
            8,
        )
        for index in range(8)
    ] == [0, 4, 2, 6, 1, 3, 5, 7]

    target = [None] * 8
    for index in range(8):
        mapped_position = (
            pylib.longevity_ordering.get_longevity_ordered_position_of_index(
                index,
                8,
            )
        )
        target[mapped_position] = index

    assert target == [0, 4, 2, 5, 1, 6, 3, 7]


def test_get_longevity_ordered_position_of_index16():
    assert [
        pylib.longevity_ordering.get_longevity_ordered_position_of_index(
            index,
            16,
        )
        for index in range(16)
    ] == [0, 8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]

    target = [None] * 16
    for index in range(16):
        mapped_position = (
            pylib.longevity_ordering.get_longevity_ordered_position_of_index(
                index,
                16,
            )
        )
        target[mapped_position] = index

    assert target == [0, 8, 4, 9, 2, 10, 5, 11, 1, 12, 6, 13, 3, 14, 7, 15]
