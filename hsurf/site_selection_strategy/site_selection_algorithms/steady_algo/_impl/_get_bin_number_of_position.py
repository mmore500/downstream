from ._get_bin_width_at_position import get_bin_width_at_position
from ._get_nth_bin_position import get_nth_bin_position
from ._get_nth_bin_width import get_nth_bin_width


def get_bin_number_of_position(position: int, surface_size: int) -> int:
    assert surface_size.bit_count() == 1  # assume power of two
    assert position < surface_size - 1  # exclude special-cased position zero

    bin_width = get_bin_width_at_position(position, surface_size)
    first_bin_width = get_nth_bin_width(0, surface_size)
    bin_segment_number = first_bin_width - bin_width
    if bin_segment_number == 0:
        return 0

    bin_segment_first_bin_number = 1 << (first_bin_width - bin_width - 1)
    assert (
        get_nth_bin_width(bin_segment_first_bin_number, surface_size)
        == bin_width
    )
    assert bin_segment_first_bin_number  # segment 0 is special-cased
    assert (
        get_nth_bin_width(bin_segment_first_bin_number - 1, surface_size)
        == bin_width + 1
    )

    bin_segment_first_bin_position = get_nth_bin_position(
        bin_segment_first_bin_number, surface_size
    )
    assert bin_segment_first_bin_position <= position

    bin_number_within_segment = (
        position - bin_segment_first_bin_position
    ) // bin_width

    return bin_segment_first_bin_number + bin_number_within_segment
