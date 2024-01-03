import interval_search as inch
import opytional as opyt

from ._get_num_bins import get_num_bins
from ._get_nth_bin_position import get_nth_bin_position


def get_bin_number_of_position(position: int, surface_size: int) -> int:
    # TODO: closed-form solution or at least binary search
    return opyt.or_value(
        inch.binary_search(
            lambda i: get_nth_bin_position(i + 1, surface_size) > position,
            0,
            get_num_bins(surface_size) - 2,
        ),
        get_num_bins(surface_size) - 1,
    )
