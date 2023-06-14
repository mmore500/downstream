import pytest

import pylib.longevity_ordering_alternating as loa


@pytest.mark.parametrize("polarity", [True, False])
def test_get_longevity_mapped_position_of_index1(polarity: bool):
    assert [
        loa.get_longevity_mapped_position_of_index(
            index,
            1,
            polarity,
        )
        for index in range(1)
    ] == [0]

    target = [None] * 1
    for index in range(1):
        mapped_position = (
            loa.get_longevity_mapped_position_of_index(
                index,
                1,
                polarity,
            )
        )
        target[mapped_position] = index

    assert target == [0]


@pytest.mark.parametrize("polarity", [True, False])
def test_get_longevity_mapped_position_of_index2(polarity: bool):
    assert [
        loa.get_longevity_mapped_position_of_index(
            index,
            2,
            polarity,
        )
        for index in range(2)
    ] == [0, 1]

    target = [None] * 2
    for index in range(2):
        mapped_position = (
            loa.get_longevity_mapped_position_of_index(
                index,
                2,
                polarity,
            )
        )
        target[mapped_position] = index

    assert target == [0, 1]


@pytest.mark.parametrize("polarity", [True, False])
def test_get_longevity_mapped_position_of_index4(polarity: bool):
    assert [
        loa.get_longevity_mapped_position_of_index(
            index,
            4,
            polarity,
        )
        for index in range(4)
    ] == (
        [0, 2, 1, 3] if polarity else [0, 2, 3, 1]
    )

    target = [None] * 4
    for index in range(4):
        mapped_position = (
            loa.get_longevity_mapped_position_of_index(
                index,
                4,
                polarity,
            )
        )
        target[mapped_position] = index

    assert target == (
        [0, 2, 1, 3] if polarity else [0, 3, 1, 2]
    )

@pytest.mark.parametrize("polarity", [True, False])
def test_get_longevity_mapped_position_of_index8(polarity):
    assert [
        loa.get_longevity_mapped_position_of_index(
            index,
            8,
            polarity,
        )
        for index in range(8)
    ] == (
        [0, 4, 2, 6, 7, 5, 3, 1]
        if polarity else
        [0, 4, 6, 2, 1, 3, 5, 7]
    )

    target = [None] * 8
    for index in range(8):
        mapped_position = (
            loa.get_longevity_mapped_position_of_index(
                index,
                8,
                polarity,
            )
        )
        target[mapped_position] = index

    assert target == (
        [0, 7, 2, 6, 1, 5, 3, 4]
        if polarity else
        [0, 4, 3, 5, 1, 6, 2, 7]
    )

@pytest.mark.parametrize("polarity", [True, False])
def test_get_longevity_mapped_position_of_index16(polarity):
    assert [
        loa.get_longevity_mapped_position_of_index(
            index,
            16,
            polarity,
        )
        for index in range(16)
    ] == (
        [0, 8, 4, 12, 14, 10, 6, 2, 1, 3, 5, 7, 9, 11, 13, 15]
        if polarity else
        [0, 8, 12, 4, 2, 6, 10, 14, 15, 13, 11, 9, 7, 5, 3, 1]
    )

    target = [None] * 16
    for index in range(16):
        mapped_position = (
            loa.get_longevity_mapped_position_of_index(
                index,
                16,
                polarity,
            )
        )
        target[mapped_position] = index

    assert target == (
        [0, 8, 7, 9, 2, 10, 6, 11, 1, 12, 5, 13, 3, 14, 4, 15]
        if polarity else
        [0, 15, 4, 14, 3, 13, 5, 12, 1, 11, 6, 10, 2, 9, 7, 8]
    )
