import interval_search as inch
import opytional as opyt

from ._get_nth_bin_position import get_nth_bin_position
from ._get_nth_bin_width import get_nth_bin_width
from ._get_num_bins import get_num_bins


def get_bin_width_at_position(position: int, surface_size: int) -> int:
    return opyt.apply_if_or_value(
        inch.binary_search(
            lambda i: get_nth_bin_position(i + 1, surface_size) > position,
            0,
            get_num_bins(surface_size) - 2,
        ),
        lambda x: get_nth_bin_width(x, surface_size),
        1,
    )
