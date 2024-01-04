import itertools as it

from ._get_nth_bin_width import get_nth_bin_width


def get_bin_width_at_position(position: int, surface_size: int) -> int:
    # related https://oeis.org/A065120
    first_bin_width = get_nth_bin_width(0, surface_size)

    position -= first_bin_width
    if position < 0:
        return first_bin_width

    # reset after special-casing the zeroth bin
    traversed = 0
    for i in it.count(1):
        bin_width = first_bin_width - i
        bin_count = 1 << (i - 1)
        traversed += bin_width * bin_count
        if position < traversed:
            return bin_width

    return 1
