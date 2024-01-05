from ._get_bin_number_of_position import get_bin_number_of_position
from ._get_nth_bin_position import get_nth_bin_position


def get_bin_offset_at_position(position: int, surface_size: int) -> int:
    bin_number = get_bin_number_of_position(position, surface_size)
    return position - get_nth_bin_position(bin_number, surface_size)
