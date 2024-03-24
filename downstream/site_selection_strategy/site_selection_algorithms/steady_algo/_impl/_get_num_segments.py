from ._get_num_bins import get_num_bins


def get_num_segments(surface_size: int) -> int:
    return get_num_bins(surface_size).bit_length()
