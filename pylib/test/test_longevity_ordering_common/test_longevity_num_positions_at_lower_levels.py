from pylib import longevity_ordering_common as loc


def test_longevity_num_positions_at_lower_levels():
    assert [*map(
        loc.get_longevity_num_positions_at_lower_levels,
        range(5)
    )] == [0, 1, 2, 4, 8]
