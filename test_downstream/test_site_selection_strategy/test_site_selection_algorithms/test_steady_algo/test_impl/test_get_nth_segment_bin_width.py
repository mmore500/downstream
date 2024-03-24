from downstream.site_selection_strategy.site_selection_algorithms.steady_algo._impl import (
    get_nth_segment_bin_width,
)


def test_get_nth_segment_bin_width():
    assert get_nth_segment_bin_width(0, 2) == 1
    assert get_nth_segment_bin_width(0, 4) == 2
    assert get_nth_segment_bin_width(1, 4) == 1
    assert get_nth_segment_bin_width(0, 8) == 3
    assert get_nth_segment_bin_width(1, 8) == 2
    assert get_nth_segment_bin_width(2, 8) == 1
    assert get_nth_segment_bin_width(0, 16) == 4
    assert get_nth_segment_bin_width(1, 16) == 3
    assert get_nth_segment_bin_width(2, 16) == 2
    assert get_nth_segment_bin_width(3, 16) == 1
    assert get_nth_segment_bin_width(0, 32) == 5
    assert get_nth_segment_bin_width(1, 32) == 4
    assert get_nth_segment_bin_width(2, 32) == 3
    assert get_nth_segment_bin_width(3, 32) == 2
    assert get_nth_segment_bin_width(4, 32) == 1
