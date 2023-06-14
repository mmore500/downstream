import pylib.longevity_ordering_alternating as loa


def test_get_longevity_num_positions_at_level():
    assert [
        *map(
            loa.get_longevity_num_positions_at_level,
            range(8),
        )
    ] == [1, 1, 2, 4, 8, 16, 32, 64]
