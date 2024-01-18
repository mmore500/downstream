from ._get_global_epoch import get_global_epoch


def get_global_num_reservations(rank: int, surface_size: int) -> int:
    """Return the number of global-level reservations at the given rank."""
    epoch = get_global_epoch(rank, surface_size)
    return get_global_num_reservations_at_epoch(epoch, surface_size)


def get_global_num_reservations_at_epoch(epoch: int, surface_size: int) -> int:
    assert surface_size.bit_count() == 1  # power of 2
    return surface_size >> (1 + epoch)
