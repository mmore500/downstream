import itertools as it

import interval_search as inch
import opytional as opyt

from ._get_nth_bin_position import get_nth_bin_position
from ._get_nth_bin_width import get_nth_bin_width
from ._get_num_bins import get_num_bins


def get_bin_width_at_position(position: int, surface_size: int) -> int:
    # related https://oeis.org/A065120
    first_bin_width = get_nth_bin_width(0, surface_size)

    position -= first_bin_width
    if position < 0:
        return first_bin_width

    for i in it.count(1):
        bin_width = first_bin_width - i
        bin_count = 1 << (i - 1)
        position -= bin_width * bin_count
        if position < 0:
            return bin_width

    return 1
