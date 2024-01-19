from hsurf.site_selection_strategy.site_selection_algorithms.steady_algo._impl import (
    get_nth_segment_bin_count,
)


def test_get_nth_segment_bin_count():
    assert get_nth_segment_bin_count(0) == 1
    assert get_nth_segment_bin_count(1) == 1
    assert get_nth_segment_bin_count(2) == 2
    assert get_nth_segment_bin_count(3) == 4
    assert get_nth_segment_bin_count(4) == 8
    assert get_nth_segment_bin_count(5) == 16
