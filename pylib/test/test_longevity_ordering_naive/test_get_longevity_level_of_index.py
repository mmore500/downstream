import pylib


def test_get_longevity_level_of_index():
    assert [
        *map(
            pylib.longevity_ordering_naive.get_longevity_level_of_index,
            range(16),
        )
    ] == [0] + [1] + [2] * 2 + [3] * 4 + [4] * 8
