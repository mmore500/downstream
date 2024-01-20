from .....pylib import bit_count_leading_ones, oeis
from ._get_nth_bin_width import get_nth_bin_width
from ._get_nth_segment_position import get_nth_segment_position
from ._get_num_positions import get_num_positions
from ._get_num_segments import get_num_segments


def get_bin_width_at_position(
    position: int,
    surface_size: int,
) -> int:
    position_from_end = get_num_positions(surface_size) - 1 - position
    assert 0 <= position_from_end < get_num_positions(surface_size)

    # must special case....
    # ... the 0th bin because the leading ones jump arbitrarily at very end
    if position < get_nth_bin_width(0, surface_size):
        return get_nth_bin_width(0, surface_size)
    # ... the bins in the rear of the leading ones only become monotonic
    # after reaching final order of magnitude, i.e., half the surface size
    elif position_from_end.bit_length() < surface_size.bit_length() - 2:
        return 1
    elif position_from_end.bit_length() < surface_size.bit_length() - 1:
        return 2

    leading_ones = bit_count_leading_ones(position_from_end)
    A083058_index = oeis.get_a083058_index_of_value(leading_ones)
    assert oeis.get_a083058_value_at_index(A083058_index) == leading_ones
    assert oeis.get_a083058_value_at_index(A083058_index - 1) < leading_ones
    assert oeis.get_a083058_value_at_index(A083058_index + 1) >= leading_ones
    assert oeis.get_a083058_value_at_index(A083058_index + 2) > leading_ones

    # this estimate is correct, or an underestimate
    # never an overestimate
    ansatz_segment_from_end = A083058_index - 2  # w/ -1 to convert to 0-indexed
    assert 0 <= ansatz_segment_from_end
    assert ansatz_segment_from_end < get_num_segments(surface_size)

    ansatz_segment = (
        get_num_segments(surface_size) - 1 - ansatz_segment_from_end
    )
    assert 1 <= ansatz_segment < get_num_segments(surface_size) - 1

    ansatz_position = get_nth_segment_position(ansatz_segment, surface_size)
    correction = position < ansatz_position

    # test if member of https://oeis.org/A000295
    # see also https://oeis.org/A083058 viz Robert G. Wilson v, Apr 19 2006
    eligible_extra_correction = leading_ones == oeis.get_a083058_value_at_index(
        A083058_index + 1
    )
    assert (
        leading_ones >= 502  # only explicitly test up to 502
        or (leading_ones in (1, 4, 11, 26, 57, 120, 247))
        == eligible_extra_correction
    )
    if eligible_extra_correction:
        assert ansatz_segment
        correction += position < (
            get_nth_segment_position(ansatz_segment - 1, surface_size)
        )

    return ansatz_segment_from_end + 1 + correction
