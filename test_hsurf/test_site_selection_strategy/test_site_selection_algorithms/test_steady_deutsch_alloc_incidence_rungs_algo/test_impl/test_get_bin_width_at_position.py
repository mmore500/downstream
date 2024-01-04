import interval_search as inch
import opytional as opyt
import pytest

from pylib import oeis
from hsurf.site_selection_strategy.site_selection_algorithms.steady_deutsch_alloc_incidence_rungs_algo._impl import (
    get_bin_width_at_position,
    get_nth_bin_position,
    get_nth_bin_width,
    get_num_bins,
    get_num_positions,
)
from pylib import bit_count_leading_ones, oeis


def _get_bin_number_of_position_expected(
    position: int, surface_size: int
) -> int:
    assert 0 <= position < get_num_positions(surface_size)
    print(surface_size, get_num_bins(surface_size))
    ub = get_num_bins(surface_size) - 2
    print(ub)
    return opyt.or_value(
        inch.binary_search_recursive(
            lambda i: get_nth_bin_position(i + 1, surface_size) > position,
            0,
            ub,  # inclusive
        ),
        get_num_bins(surface_size) - 1,  # special case upper bound
    )


def _get_bin_width_at_position_expected(
    position: int, surface_size: int
) -> int:
    assert 0 <= position < get_num_positions(surface_size)
    return opyt.apply_if_or_value(
        inch.binary_search_recursive(
            lambda i: get_nth_bin_position(i + 1, surface_size) > position,
            0,
            get_num_bins(surface_size) - 2,  # inclusive
        ),
        lambda x: get_nth_bin_width(x, surface_size),
        1,  # special case upper bound
    )


@pytest.mark.parametrize("surface_size", [2**i for i in range(16)])
def test_get_bin_width_at_position_expected(surface_size: int):
    for position in range(get_num_positions(surface_size)):
        bin_number = _get_bin_number_of_position_expected(
            position, surface_size
        )
        bin_width = get_nth_bin_width(bin_number, surface_size)
        assert bin_width == _get_bin_width_at_position_expected(
            position, surface_size
        )


@pytest.mark.parametrize("surface_size", [2**i for i in range(3, 19)])
def test_get_bin_width_at_position(surface_size: int):
    for position in range(0, surface_size - 1):
        assert 0 <= position < surface_size - 1
        bin_width = _get_bin_width_at_position_expected(position, surface_size)
        estimated = get_bin_width_at_position(position, surface_size)
        assert estimated == bin_width


@pytest.mark.parametrize("surface_size", [2**i for i in range(3, 19)])
def test_oeis_pattern(surface_size: int):
    last_bin_width = surface_size.bit_length()
    last_leading_ones = surface_size.bit_length()
    for position in range(0, get_num_positions(surface_size)):
        position_from_end = get_num_positions(surface_size) - 1 - position
        assert 0 <= position_from_end < get_num_positions(surface_size)

        bin_width = _get_bin_width_at_position_expected(position, surface_size)
        leading_ones = bit_count_leading_ones(position_from_end)
        assert bin_width <= last_bin_width  # iterating position fwd
        last_bin_width = bin_width
        last_leading_ones = leading_ones
        index = None

        assert position_from_end.bit_length() < surface_size.bit_length()
        assert position.bit_length() < surface_size.bit_length()
        if position < get_nth_bin_width(0, surface_size):
            estimated = get_nth_bin_width(0, surface_size)
            assert estimated == bin_width
        elif position_from_end.bit_length() < surface_size.bit_length() - 2:
            estimated = 1
            assert estimated == bin_width
        elif position_from_end.bit_length() < surface_size.bit_length() - 1:
            estimated = 2
            assert estimated == bin_width
        else:
            assert leading_ones <= last_leading_ones  # iterating position fwd
            index = oeis.get_a083058_index_of_value(leading_ones)
            estimated = index - 1
        assert estimated >= 0

        assert estimated <= bin_width  # never overestimate
        assert abs(estimated - bin_width) < 3  # off by no more than two
