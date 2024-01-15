from ._get_global_epoch import get_global_epoch


def get_global_num_reservations(rank: int, surface_size: int) -> int:
    """Return the number of global-level reservations at the given rank."""
    assert surface_size.bit_count() == 1  # power of 2
    return surface_size >> (1 + get_global_epoch(rank, surface_size))
